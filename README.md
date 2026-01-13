## SNP2Pheno
Study Project MBI 2025

This program is part of a study project within the MBI degree program at the University of Applied Sciences Upper Austria, Hagenberg Campus. The project's objective is to analyze an individual's genotype — specifically, known SNPs within their genetic sequence — to infer phenotypic traits. The ultimate goal is to generate a probabilistic facial reconstruction based on genetic markers, provide an overview of potential disease risks, and estimate the individual's likely ancestral origins.

# Setup
The project requires a 'config.cmake' file in the same driectory as the 'CMakeLists.txt'.
It is necessary to specify the installation path for the Qt Framework.
Furthermore, the file includes a Prefix, depending on the OS you are using.
Here you can see how the 'config.cmake' should look like:

file: config.cmake
```
set(CMAKE_PREFIX_PATH "/Users/georg/Qt/6.9.3/macos/lib/cmake")

# For macOS using CMake in the CLion IDE
set(OS_PREFIX "../")

# For Windows using CMake in Visual Studio (2022) with the MinGW compiler
# set(OS_PREFIX "../../../")
```

# License
This project is licensed under the MIT License.

This project uses the Qt framework under the terms of the GNU Lesser General Public License (LGPL) v3.0.
See [LICENSE.LGPLv3](./LICENSE.LGPLv3) for the full license text.

The Qt libraries are dynamically linked and not modified.
