using Ionic.Zip;
using Samples;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls.Primitives;
using System.Windows.Media.Imaging;

namespace ServerApp
{
    class Transfer
    {

        static Socket Datareceiver_socket;
        static TcpClient tcpcl;
        static TcpListener server;

        static volatile bool breakTransfer = false;
        static volatile bool iscopy = false;
        static volatile bool ispaste = false;

        #region Property

        public static bool BreakTransfer
        {
            get { return breakTransfer; }
            set { breakTransfer = value; }
        }

        public static bool Iscopy
        {
            get { return iscopy; }
            set { iscopy = value; }
        }

        public static bool Ispaste
        {
            get { return ispaste; }
            set { ispaste = value; }
        }

        #endregion

        #region Utilities

        public static void CloseThServer()
        {
            if (server != null) server.Stop();
        }


        /*Rimozione attributi di un file*/
        private static FileAttributes RemoveAttribute(FileAttributes attributes, FileAttributes attributesToRemove)
        {
            return attributes & ~attributesToRemove;
        }

        /*Scasione directory e rimozione da ogni file dell'attributo ReadOnly*/
        private static void ClearReadOnly(DirectoryInfo parentDirectory)
        {

            try
            {
                if (parentDirectory != null)
                {
                    parentDirectory.Attributes = FileAttributes.Normal;
                    foreach (FileInfo fi in parentDirectory.GetFiles())
                    {
                        fi.Attributes = FileAttributes.Normal;
                    }
                    foreach (DirectoryInfo di in parentDirectory.GetDirectories())
                    {
                        ClearReadOnly(di);
                    }
                }
            }
            catch (Exception)
            {

                throw;
            }
        }


        /*Verifica se la connessione è stata chiusa*/
        public static int CanRead(TcpClient tcpcl)
        {
            bool part1 = tcpcl.Client.Poll(1000, SelectMode.SelectRead);
            bool part2 = (tcpcl.Client.Available == 0);
            if (part1 && part2)
            {
                return 1;
            }
            return 0;
        }




        public static void DeleteFolderContent(String name)
        {


            try
            {
                
                string[] Listfex = Directory.GetFiles(name, "*.*");
                string[] Listdex = Directory.GetDirectories(name, "*.*");
              
                foreach (string ff in Listfex)
                {
                    //rimuovo dai file attributo ReadOnly
                    FileAttributes attributes = File.GetAttributes(ff);
                    if ((attributes & FileAttributes.ReadOnly) == FileAttributes.ReadOnly)
                    {
                        attributes = RemoveAttribute(attributes, FileAttributes.ReadOnly);
                        File.SetAttributes(ff, attributes);
                    }
                  /* Eliminazione file*/
                    File.Delete(ff);
                }
               
                foreach (string fd in Listdex)
                {
                    System.IO.DirectoryInfo dr = new System.IO.DirectoryInfo(fd);
                    ClearReadOnly(dr);
                     /* Eliminazione cartelle*/ 
                    Directory.Delete(fd, true);
                }

            }
            catch (Exception)
            {

                return;
            }

        }

        #endregion

        #region Eventi

        /*Gestioni operazione copia remota*/
        public static bool EventoClipboardCopy()
        {

            try
            {
                /*Verifico che la clipboard sia piena*/
                if (System.Windows.Clipboard.ContainsAudio() || System.Windows.Clipboard.ContainsImage() || System.Windows.Clipboard.ContainsText() || System.Windows.Clipboard.ContainsFileDropList())
                {

                    Thread r = new Thread(new ThreadStart(datatransfer));
                    r.SetApartmentState(ApartmentState.STA);
                    r.Start();
                }
                return true;

            }
            catch (OutOfMemoryException)
            {
                Application.Current.Dispatcher.Invoke(System.Windows.Threading.DispatcherPriority.Normal, new Action(delegate()
                {
                    FancyBalloon fp = new FancyBalloon();
                    fp.tit.Text = "ERROR";
                    fp.msg.Text = "Non c'è abbastanza memoria, chiudi qualche applicazione";
                    MainWindow.tbi.ShowCustomBalloon(fp, PopupAnimation.Slide, 5000);
                }));
      
                return false;
            }

        }




        #endregion

        #region ReceiveFunction

        public static int ReceiveIntFromServer(NetworkStream st, int len)
        {
            byte[] dim = new byte[len];

            int readedbyte = 0;

            /*Acquisizione dimensione del flusso dati*/
            while (readedbyte != len)
                readedbyte += st.Read(dim, readedbyte, len - readedbyte);
            /*Conversione in formato di rete*/
            if (BitConverter.IsLittleEndian)
                Array.Reverse(dim);
            return BitConverter.ToInt32(dim, 0);
        }


        public static void readDataFromServer(Socket s1, MemoryStream m, int dimi, BinaryWriter bw)
        {

            /*Buffer per la lettura dei dati*/
            Byte[] app = new Byte[8500];
            int tot = 0, rit = 0;

            /*Ciclo lettura da socket e scrittura sul memory stream*/

            s1.ReceiveTimeout = 10000;
            int tent = 5;

            for (; ; )
            {
                while (tent > 0 && breakTransfer == false)
                {
                    try
                    {
                        rit = s1.Receive(app, 0, 8000, SocketFlags.None);
                        if (rit <= 0)
                        {
                            throw new Exception();

                        }
                        tent = 5;
                        break;

                    }
                    catch (Exception)
                    {

                        tent--;
                        if (tent == 0)
                        {

                            breakTransfer = true;
                            throw;
                        }
                    }
                }

                if(m==null)
                    bw.Write(app, 0, rit);
                else
                    m.Write(app, 0, rit);

                tot += rit;
                if (tot >= dimi) break;
            }

        }

       

        #endregion

        #region SendFunction

        public static void sendIntToServer(int Service_type, NetworkStream st)
        {

            try
            {
                byte[] typeBytes = BitConverter.GetBytes(Service_type);
                /*conversione in formato di rete*/
                if (BitConverter.IsLittleEndian)
                    Array.Reverse(typeBytes);

                st.Write(typeBytes, 0, typeBytes.Length);

            }
            catch (Exception)
            {

                throw;

            }

        }


        public static void sendDataToServer(MemoryStream m, NetworkStream st, int length, FileStream fs)
        {

            Byte[] buff = new Byte[8500];
            /*variabili utilizzate per ciclo trasferimento dati */
            int ris = 0, tot = 0;
            /*Ciclo lettura dati e scrittura su socket*/
            try
            {
               

                /*Trasferimento dati */
                for (; ; )
                {
                    if(m==null)
                        ris = fs.Read(buff, 0, 8000);
                    else
                        ris = m.Read(buff, 0, 8000);

                    st.Write(buff, 0, ris);

                    tot += ris;
                    if (tot >= length) break;
                }
            }
            catch (Exception)
            {
                throw;
            }


        }



        #endregion

        #region Graphic

        public static void UpdateGuiTransferDone()
        {

            Application.Current.Dispatcher.Invoke(System.Windows.Threading.DispatcherPriority.Normal, new Action(delegate()
            {
                FancyBalloon fp = new FancyBalloon();
                fp.tit.Text = "Information";
                fp.msg.Text = "Contenuto clipboard aggiornato!";
                MainWindow.tbi.ShowCustomBalloon(fp, PopupAnimation.Slide, 5000);
            }));


        }


        #endregion


        #region Importazione clipboard dal client

        /*Handler  per ricezione dati clipboard lato server*/
        private static void clipboardhandler()
        {
         
            ispaste = true;

            TcpClient tcpcl = null;
            NetworkStream st = null;
            MemoryStream m = null;

            try
            {

                tcpcl = new TcpClient();
                tcpcl.Client = Datareceiver_socket;
                /*Creazione stream tcp*/
                st = tcpcl.GetStream();

                /*Lettura tipo servizio richiesto*/
                int typeserv=ReceiveIntFromServer(st, 4);
               

                /*tipi servizio :
                 * 1 testo
                 * 2 image
                 * 3 audio
                 * 4 file
                 * */

                switch (typeserv)
                {

                    case 1:
                        {
                            /*TESTO*/
                           
                            /*Lettuara dimensioni */
                            int dimi=ReceiveIntFromServer(st, 4);                            
                            Byte[] buff = new Byte[dimi];                     
                            m = new MemoryStream(buff);

                            /*Lettura dati*/
                            readDataFromServer(Datareceiver_socket, m, dimi, null);
                            
                            if (breakTransfer == true) break;

                            String str = Encoding.Unicode.GetString(buff);
                            
                            Clipboard.Clear();
                            /*Update clipboard Server*/
                            DataObject d = new DataObject();
                            d.SetData(DataFormats.Rtf, str);
                            d.SetData(DataFormats.Text, str);
                            Clipboard.SetDataObject(d, true);

                            UpdateGuiTransferDone();
                            
                            break;
                        }
                    case 2:
                        {
                            /*IMMAGINE*/

                            /*Lettura dimensioni */
                            int dimi=ReceiveIntFromServer(st, 4);
                            
                          
                            m = new MemoryStream();
                            BinaryWriter bw = new BinaryWriter(m);

                            /*Lettura dati */
                            readDataFromServer(Datareceiver_socket, null, dimi, bw);


                            if (breakTransfer == true) break;

                           /*Riavvolgimento stream*/
                            bw.Seek(0, 0);
                            /*Decodifica immagine*/
                            JpegBitmapDecoder decoder = new JpegBitmapDecoder(m, BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.Default);
                            BitmapSource bitmapSource = decoder.Frames[0];

                            /*Aggiorno clipboard  server*/
                            Clipboard.Clear();
                            Clipboard.SetImage(bitmapSource);

                            UpdateGuiTransferDone();

                            bw.Close();
                            
                            break;
                        }
                    case 3:
                        {
                            /*AUDIO*/

                            /*Lettura dimensioni */
                            int dimi = ReceiveIntFromServer(st, 4);          

                            m = new MemoryStream();

                            /*Lettura dati */
                            readDataFromServer(Datareceiver_socket, m, dimi, null);
                          
                            if (breakTransfer == true) break;

                            /*Aggiorno clipboard  server*/
                            Clipboard.Clear();
                            Clipboard.SetAudio(m);

                            UpdateGuiTransferDone();

                            break;
                        }
                    case 4:
                        {
                            /*FILE*/
                            
                            String str = "MyZipFile.zip";
                            
                            
                            /*Lettura dimensioni */
                            int dimi = ReceiveIntFromServer(st, 4);

                            
                           
                            /*Setto il path del file nella variabile result*/
                            String result = "";
                           
                            if (!Directory.Exists("TempIn"))
                            {
                                /* Creazione cartella temporanea*/
                                DirectoryInfo di = Directory.CreateDirectory("TempIn");
                                System.IO.File.SetAttributes("TempIn", FileAttributes.Hidden);
                            }
                            else
                                DeleteFolderContent("TempIn");

                            result += System.IO.Path.GetFullPath("TempIn");
                            result += "\\" + str;

                           
                          /*Creazione file */
                            FileStream fs = null;
                            BinaryWriter bw = null;                            
                            try
                            {
                                fs = File.Create(result);
                                bw = new BinaryWriter(fs);
                                readDataFromServer(Datareceiver_socket, null, dimi, bw);

                            }
                            catch (Exception)
                            {

                                throw;
                            }
                            finally
                            {

                                if (bw != null)
                                {
                                    bw.Close();
                                    bw = null;
                                }
                                if (fs != null)
                                {
                                    fs.Close();
                                    fs = null;
                                }
                            }



                            if (breakTransfer == true) break;

                            /*Creazione cartella dove estrarre il file zip*/
                            if (!Directory.Exists("Extract"))
                            {
                                DirectoryInfo di = Directory.CreateDirectory("Extract");
                                System.IO.File.SetAttributes("Extract", FileAttributes.Hidden);
                            }
                            else
                                DeleteFolderContent("Extract");

                            /*Estrazione file zip*/
                            using (ZipFile zip = ZipFile.Read(result))
                            {
                                zip.ExtractAll(".\\Extract");
                            }

                            /*Inserisco ogni file nella cartella extract nella clipboard*/
                            StringCollection scex = new StringCollection();
                            string[] Listfile = Directory.GetFiles("Extract", "*.*");
                            string[] Listdir = Directory.GetDirectories("Extract", "*.*");
                            /*Aggiunta i file*/
                            foreach (string fa in Listfile)
                            {
                                scex.Add(System.IO.Path.GetFullPath(fa));
                            }
                            /*Aggiunta cartelle*/
                            foreach (string fb in Listdir)
                            {
                                scex.Add(System.IO.Path.GetFullPath(fb));
                            }
                            /*Aggiornamento clipboard*/
                            Clipboard.SetFileDropList(scex);

                            UpdateGuiTransferDone();
                            
                            break;
                        }

                    default:
                        break;
                }

            }
            catch (Exception)
            {
                
            }
            finally
            {
                //chiudo stream memory
                if (m != null)
                {
                    m.Close();
                    m = null;
                }
                //chiudo stream rete
                if (st != null)
                {
                    st.Close();
                    st = null;
                }
                //chiudo connessione
                if (tcpcl != null)
                {
                    tcpcl.Close();
                    tcpcl = null;
                }

                breakTransfer = false;
                ispaste = false;
            }
        }


        #endregion

        #region Esportazione clipboard al client

        //thread gestione trasferimento dati clipboard da server a client
        public static void datatransfer()
        {
            iscopy = true;
            NetworkStream st = null;
            MemoryStream m = null;

            try
            {
                /*Acquisisco ip del client*/
                IPAddress ipr = IPAddress.Parse(((IPEndPoint)MainWindow.s.RemoteEndPoint).Address.ToString());
                tcpcl = new TcpClient(ipr.ToString(), 1999);
                /*Settaggio dimensioni buffer*/
                tcpcl.Client.ReceiveBufferSize = 8192;
                tcpcl.Client.SendBufferSize = 8192;

                /*tipi servizio : 
                 * 1 text
                 * 2 image
                 * 3 audio
                 * 4 file
                 * */

                int typeserv = 0;
                /*Creazione stream tcp*/
                st = tcpcl.GetStream();


                /*TESTO*/
                if (System.Windows.Clipboard.ContainsText())
                {
                     
                    byte[] data;
                    /*Settaggio tipo servizio*/
                    typeserv = 1;

                    /*Distinzione tipo formato*/
                    if (System.Windows.Clipboard.ContainsText(System.Windows.TextDataFormat.Rtf))
                        data = Encoding.Unicode.GetBytes(System.Windows.Clipboard.GetText(System.Windows.TextDataFormat.Rtf));
                    else
                        data = Encoding.Unicode.GetBytes(System.Windows.Clipboard.GetText());

                    /*Invio tipo servizio*/
                    sendIntToServer(typeserv, st);


                    /*Invio lunghezza dati*/
                    sendIntToServer(data.Length, st);

                    
                    Byte[] app = new Byte[8500];
                    m = new MemoryStream(data);
                    
                    /*Ciclo lettura da memoria e scrittura su socket*/
                    sendDataToServer(m, st, data.Length, null);
                    
                }


                /*IMMAGINE*/

                if (System.Windows.Clipboard.ContainsImage())
                {
                    /*Settaggio tipo servizio*/
                    typeserv = 2;

                    /*Invio tipo servizio*/
                    sendIntToServer(typeserv, st);

                    
                    MemoryStream stream = new MemoryStream();

                    /*Acquisisco immagine dalla clipboard*/
                    BitmapSource bitmapSource = System.Windows.Clipboard.GetImage();
                    JpegBitmapEncoder encoder = new JpegBitmapEncoder();
                    encoder.Frames.Add(BitmapFrame.Create(bitmapSource));
                    encoder.Save(stream);
                    byte[] buff = stream.ToArray();

                    /*Invio dimensioni a Client.server*/
                    sendIntToServer(buff.Length, st);
                                       
                    m = new MemoryStream(buff);

                    /*Trasferimento */
                    sendDataToServer(m, st,(int)m.Length, null);
                    

                }

                /*AUDIO*/

                if (System.Windows.Clipboard.ContainsAudio())
                {


                    /*Settaggio tipo servizio*/
                    typeserv = 3;
                    
                    /*Invio tipo servizio*/
                    sendIntToServer(typeserv, st);

                   
                    /*Acquisisco stream audio*/
                    Stream stream = System.Windows.Clipboard.GetAudioStream();
                    m = new MemoryStream();
                    stream.CopyTo(m);

                    /*Invio dimensioni*/
                    sendIntToServer((int)m.Length, st);
                  
                    /*Trasferimento*/
                    sendDataToServer(m, st, (int)m.Length, null);

                }


                /*FILE*/
                if (System.Windows.Clipboard.ContainsFileDropList())
                {

                
                    StringCollection sc = System.Windows.Clipboard.GetFileDropList();
                    ZipFile zip = new ZipFile();
                    zip.CompressionLevel = Ionic.Zlib.CompressionLevel.BestSpeed;

                    /*Settaggio tipo servizio*/
                     typeserv = 4;
                     /*Invio tipo servizio*/
                    sendIntToServer(typeserv, st);

                    /*Acquisisco percorsi clipboard*/
                    foreach (String str in sc)
                    {

                        string path = "";

                        /*Caso cartella*/
                        if (System.IO.Directory.Exists(str))
                        {   
                            String stt = str;
                            stt += "\\"; 
                            path = System.IO.Path.GetFileName(System.IO.Path.GetDirectoryName(stt));
                            
                            zip.AddDirectory(str, path);
                        }
                        else
                        {    /*Caso file*/
                            
                            zip.AddFile(str, ".\\");
                        }

                    }

                    /*Creazione cartella per file in uscita*/
                    if (!Directory.Exists("TempOut"))
                    {
                        DirectoryInfo di = Directory.CreateDirectory("TempOut");
                        System.IO.File.SetAttributes("TempOut", FileAttributes.Hidden);
                    }

                    string w = "TempOut\\MyZipFile.zip";
                    zip.Save(w);                
                   
                    FileStream fs = File.OpenRead(w);
                    FileInfo fi = new FileInfo(w); 

                    /*Invio dimensione file*/
                    sendIntToServer(Convert.ToInt32(fi.Length),st);                    
                    try
                    {    /*Trasferimento*/
                        sendDataToServer(null, st, Convert.ToInt32(fi.Length), fs);

                    }
                   
                    catch (Exception)
                    {

                    }
                    finally
                    {

                        if (fs != null)
                        {
                            fs.Close();
                            fs = null;
                        }

                    }

                }

            }
            catch (Exception)
            {
                
            }
            finally
            {

                if (m != null)
                {
                    m.Close();
                    m = null;
                }
                if (st != null)
                {
                    st.Close();
                    st = null;
                }

                iscopy = false;
            }
        }

        #endregion

        #region EntryPoint


        //server ricezione dati
        private static void handler()
        {

            try
            {

                IPAddress ipAd = null;
                String listenerip = Utilities.GetActiveIP();
                if (!listenerip.Equals(""))
                {
                    ipAd = IPAddress.Parse(listenerip);
                }
                else
                {
                    throw new Exception();
                }
               

                /*Avvio server in ascolto richieste entranti*/
                server = new TcpListener(ipAd, 1998);
                server.Start();
               /*Setto dimensioni buffer*/
                server.Server.ReceiveBufferSize = 8192;
                server.Server.SendBufferSize = 8192;
                /*Server iterativo, Gestisce una richiesta una alla volta*/
                for (; ; )
                {
                    Datareceiver_socket = server.AcceptSocket();
                    try
                    {
                        
                        Thread t = new Thread(new ThreadStart(clipboardhandler));
                        t.SetApartmentState(ApartmentState.STA);
                        t.Start();
                        t.Join();
                    }
                    catch (OutOfMemoryException)
                    {
                        Application.Current.Dispatcher.Invoke(System.Windows.Threading.DispatcherPriority.Normal, new Action(delegate()
                        {
                            FancyBalloon fp = new FancyBalloon();
                            fp.tit.Text = "ERROR";
                            fp.msg.Text = "Non c'è abbastanza memoria, chiudi qualche applicazione";
                            MainWindow.tbi.ShowCustomBalloon(fp, PopupAnimation.Slide, 5000);
                        }));
                        
                        continue;
                    }
                }
            }
            catch (Exception)
            {

            }

        }

        /*Metodo statico che fa partire il socket server*/
        public static bool Start()
        {
            try
            {
                Thread t = new Thread(new ThreadStart(handler));
                t.Start();
                return true;
            }
            catch (OutOfMemoryException)
            {
                Application.Current.Dispatcher.Invoke(System.Windows.Threading.DispatcherPriority.Normal, new Action(delegate()
                {
                    FancyBalloon fp = new FancyBalloon();
                    fp.tit.Text = "ERROR";
                    fp.msg.Text = "Non c'è abbastanza memoria, chiudi qualche applicazione";
                    MainWindow.tbi.ShowCustomBalloon(fp, PopupAnimation.Slide, 5000);
                }));
               
                return false;
            }
        }


        #endregion
    
    }
}
