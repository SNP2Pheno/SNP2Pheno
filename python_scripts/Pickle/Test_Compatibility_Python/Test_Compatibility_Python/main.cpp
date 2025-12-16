#include <iostream>
#include <array>
#include <string>
#include <vector>
#include <fstream>
int main() {
    std::vector<std::string> arg;
    // TODO: read pkl file path and second argument (model rsIDs) from DB!
    arg.push_back("RF_eyecolor.pkl");
    arg.push_back("rs12913832:A,rs12896399:G,rs1408799:C");

    //TODO: personData.txt doesn´t exist - the file format for the person data is yet to be determined
    arg.push_back("personData.txt");
    arg.push_back("rs12203592:CC,CT,TT");


    std::string cmd = "python pkl_load.py " + arg[0] + " " + arg[1] + " " + arg[2] + " " + arg[3];
    std::array<char, 128> buffer{};
    std::string result;

    FILE* pipe = _popen(cmd.c_str(), "r");

    if (!pipe) {
        std::cerr << "Failed to run Python script.\n";
        return 1;
    }

    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        result += buffer.data();
    }

    _pclose(pipe);

    std::string s = result;

    std::ofstream MyFile("filename.txt");
    MyFile << s;
    std::cout << result;

    return 0;
}