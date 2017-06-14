#include <iostream>
#include <gtest/gtest.h>

class Account{
  
  public: int balance;
  
  Account(){
    
  }
  
  explicit Account(const int b):balance(b){
    
    
    
  }
  
};

TEST(AccountTest, first){
  
  Account acc(0);
  EXPECT_EQ(0,acc.balance);
  
}

TEST(AccountTest, second){

  EXPECT_EQ(0,0);
  EXPECT_EQ(1,1);

}

int main(int argc, char **argv) {
    
   testing::InitGoogleTest(&argc,argv);
   
   return RUN_ALL_TESTS();
  
    
}
