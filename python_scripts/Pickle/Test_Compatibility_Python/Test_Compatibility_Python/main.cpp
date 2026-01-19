#include <iostream>
#include <array>
#include <string>
#include <vector>
#include <fstream>
#include <QSqlDatabase>


int main() {
    // NOTE: this DB access code is not reliably formatted correctly
    // open DB
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("database.db");
    if (!db.open()) {
        // TODO: handle error
    }
    
    // getting the path
    int ModelID = 1;
    std::string path;

    SQLite::Statement query(db, "SELECT Path_To_Model FROM Model_Table WHERE ID=", ModelID);
    
    while (query.executeStep()) {
        path = query.getColumn(0).getString();
    }

    // getting the model rsIDs
    std::string rsIDs;
    SQLite::Statement query(db, "SELECT ID, Allele_1, Allele_2"
                                "FROM Allele_Table a INNER JOIN SNP_TABLE s ON a.ID=s.rs_ID"
                                "INNER JOIN RELEVANT_SNPS_CLASS_TABLE r ON s.rs_ID=r.SNP_ID"
                                "WHERE r.Model_ID=", ModelID);
    while (query.executeStep()) {
        rsIDs = query.getColumn(0).getString();
    } // TODO: need to make sure that the result here is formatted correctly


    std::vector<std::string> arg;

    arg.push_back(path); // RF_eyecolor.pkl
    arg.push_back(rsIDs); // rs12913832:A,rs12896399:G,rs1408799:C

    //TODO: personData.txt doesn´t exist --> it should be either .txt or .vcf
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