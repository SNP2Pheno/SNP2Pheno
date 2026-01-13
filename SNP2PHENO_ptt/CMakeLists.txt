cmake_minimum_required(VERSION 3.30)
project(SNP2PHENO_ptt)

include (config.cmake)

set(CMAKE_CXX_STANDARD 23)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick Qml QuickControls2 Sql QmlModels)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

include(FetchContent)

FetchContent_Declare(
        snp2pheno_vcfparser
        GIT_REPOSITORY https://github.com/SNP2Pheno/vcfParser.git
        GIT_TAG 33925b3 # Change this commit hash if a newer version of the parser is available
)

FetchContent_MakeAvailable(snp2pheno_vcfparser)

add_library(vcfparser_lib
        ${snp2pheno_vcfparser_SOURCE_DIR}/vcfParser/VCFParser.cpp
        ${snp2pheno_vcfparser_SOURCE_DIR}/vcfParser/utils.cpp
        ${snp2pheno_vcfparser_SOURCE_DIR}/vcfParser/HeaderParsing.cpp
        ${snp2pheno_vcfparser_SOURCE_DIR}/vcfParser/RecordsParsing.cpp
)

target_include_directories(vcfparser_lib
        PUBLIC
        ${snp2pheno_vcfparser_SOURCE_DIR}/vcfParser
)

add_executable(SNP2PHENO_ptt
        main.cpp
        controller/Controller.cpp
        controller/Controller.h
        controller/headers/FileParsedState.h
        controller/headers/FileData.h
)

# This makes the constants available in .cpp files (mainly main.cpp)
target_compile_definitions(SNP2PHENO_ptt
        PRIVATE
        OS_PREFIX=\"${OS_PREFIX}\"
)

target_link_libraries(SNP2PHENO_ptt
        PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Quick
        Qt6::Qml
        Qt6::QuickControls2
        Qt6::Sql
        Qt6::QmlModels
        vcfparser_lib
)
