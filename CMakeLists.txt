cmake_minimum_required(VERSION 2.6)
project(mytest)

                    
# compite GTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})




add_executable(mytest main.cpp)
target_link_libraries(mytest ${GTEST_LIBRARIES} pthread)

install(TARGETS mytest RUNTIME DESTINATION bin)

enable_testing()
add_test(NAME first COMMAND mytest)

add_test(NAME second COMMAND mytest)
