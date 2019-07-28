#include <iostream>
#include <string>
#include <set>

using namespace std;

set <pair <int, pair <string, string> > > st;

int main() {
    string s1, s2;
    int t;
    while (cin >> s1 >> s2 >> t) {
        if (s1 > s2) {
            swap(s1, s2);
        }
        st.insert({t, {s1, s2}});
    }
    for (auto a : st) {
        cout << a.second.first << " " << a.second.second << " " << a.first << endl;
    }
    return 0;
}
