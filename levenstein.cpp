#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

int m(char a, char b) {
    if (a == b) {
        return 0;
    }
    return 1;
}

int f(string &s1, string &s2) {
    vector <vector <int> > dp(s1.size() + 1, vector <int> (s2.size() + 1, 0));
    for (int i = 0; i <= s1.size(); ++i) {
        for (int j = 0; j <= s2.size(); ++j) {
            if (i == 0 && j == 0) {
                dp[i][j] = 0;
                continue;
            }
            if (i == 0) {
                dp[i][j] = j;
                continue;
            }
            if (j == 0) {
                dp[i][j] = i;
                continue;
            }
            dp[i][j] = min(min(dp[i][j - 1] + 1, dp[i - 1][j] + 1), dp[i - 1][j - 1] + m(s1[i - 1], s2[j - 1]));
        }
    }
    return dp[s1.size()][s2.size()];
}

void read(string &ans, string file_name) {
    ifstream in(file_name);
    string s;
    while (in >> s) {
        ans += s;
        ans += '\n';
    }
}

int main(int argc, char *argv[]) {
    string s1, s2;
    read(s1, argv[1]);
    read(s2, argv[2]);
    //cout << s1 << endl << s2 << endl;
    cout << f(s1, s2);
    return 0;
}
