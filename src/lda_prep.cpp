#include <iostream>
#include <sstream>
#include <string>
#include <boost/algorithm/string.hpp>

using namespace std;

bool has_at_least_one_alpha_numeric(string &token) {
    for(auto& ch : token)
        if (isalnum(ch))
            return true;
    return false;
}

int main(int argc, char **argv) {
    string line;
    string token;
    while (getline(cin, line)) {
        // tokenise line
        istringstream iss(line, istringstream::in);
        // read and write primary_id & secondary_id
        iss >> token;
        cout << token;
        iss >> token;
        cout << " " << token;
        while (iss >> token) {
            // ignore short strings
            if (token.length() < 3)
                continue;
            // must have at least one alpha
            if (!has_at_least_one_alpha_numeric(token))
                continue;
            // downcase
            boost::algorithm::to_lower(token);
            // emit
            cout << " " << token;
        }
        cout << "\n";
    }
    return 0;
}
