#include "../headers/vcf_to_snp.h"
#include <QFile>
#include <QTextStream>
#include <QUrl>


// Helper function to determine if both ref and alt are single characters.
static bool isSNP(const QString& ref, const QString& alt) {
    return (ref.length() == 1 && alt.length() == 1);
}

VcfToSnp::VcfToSnp(QObject* parent)
    : QObject(parent)
{
}

QStringList VcfToSnp::parseVCF(const QString& filePath) {
    QStringList result;

    // Convert a file URL (e.g., "file:///C:/...") to a local file path
    QString localFilePath = filePath;
    if (filePath.startsWith("file://")) {
        localFilePath = QUrl(filePath).toLocalFile();
    }

    QFile file(localFilePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return result;
    }

    QTextStream in(&file);
    int lineCount = 0;
    while (!in.atEnd()) {
        QString line = in.readLine();
        ++lineCount;

        if (line.isEmpty() || line.startsWith('#'))
            continue;

        // VCF file columns are expected to be tab-delimited.
        QStringList columns = line.split('\t');
        if (columns.size() < 5)
            continue;

        QString chrom = columns[0];
        QString id = columns[2];
        QString ref = columns[3];
        QString alt = columns[4];

        if (id != "." && isSNP(ref, alt)) {
            // Expected id format: "chrXX-...-SNV->snp1>snp2<snp3>..."
            int arrowIndex = id.indexOf("->");
            if (arrowIndex != -1) {
                QString leftPart = id.left(arrowIndex);      // e.g. "chr21-40205284-SNV"
                QString rightPart = id.mid(arrowIndex + 2);    // e.g. "s865813>s876698<s875018>s865816-1"

                // Extract the chromosome label (assumes leftPart starts with "chrXX")
                int dashIndex = leftPart.indexOf("-");
                QString chrLabel = (dashIndex != -1) ? leftPart.left(dashIndex) : leftPart;

                // Split the right part using both '>' and '<' as delimiters.
                QString token;
                QStringList snpTokens;
                for (int i = 0; i <= rightPart.length(); ++i) {
                    if (i == rightPart.length() || rightPart[i] == '>' || rightPart[i] == '<') {
                        if (!token.isEmpty()) {
                            snpTokens << token;
                        }
                        token.clear();
                    }
                    else {
                        token.append(rightPart[i]);
                    }
                }

                // For each SNP token, prepend the chromosome label and add to the result.
                for (const QString& snp : snpTokens) {
                    QString finalSnp = chrLabel + " " + snp;
                    result << finalSnp;
                }
            }
            else {
                // If the expected arrow ("->") isn't found, add the raw id.
                result << id;
            }
        }
    }
    file.close();
    return result;
}
