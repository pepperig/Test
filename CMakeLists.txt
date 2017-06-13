cmake_minimum_required(VERSION 2.6)
project(mytest)

                  
# compite GTest
#find_package(GTest REQUIRED)
#include_directories(${GTEST_INCLUDE_DIRS})

set(GOOGLETEST_ROOT external/googletest/googletest CACHE STRING "Google Test source root")

include_directories(
    ${PROJECT_SOURCE_DIR}/${GOOGLETEST_ROOT}
    ${PROJECT_SOURCE_DIR}/${GOOGLETEST_ROOT}/include
    )

set(GOOGLETEST_SOURCES
    ${PROJECT_SOURCE_DIR}/${GOOGLETEST_ROOT}/src/gtest-all.cc
    ${PROJECT_SOURCE_DIR}/${GOOGLETEST_ROOT}/src/gtest_main.cc
)

add_library(googletest ${GOOGLETEST_SOURCES}) 

add_executable(mytest main.cpp)
#target_link_libraries(mytest ${GTEST_LIBRARIES} pthread)
target_link_libraries(mytest googletest pthread)

install(TARGETS mytest RUNTIME DESTINATION bin)

enable_testing()
add_test(NAME first COMMAND mytest)

add_test(NAME second COMMAND mytest)
