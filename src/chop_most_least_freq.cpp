#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <iterator>
#include <stdlib.h>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/program_options.hpp>

using namespace std;
using namespace boost::program_options;

typedef set<string> s_s;
typedef map<string, unsigned int> m_s_ui;

int main(int argc, char **argv)
{
    // arg handling
    float lower_bound_percentage, upper_bound_percentage;
    string input_file, keep_token;
    options_description opts("opts");
    opts.add_options()
        ("help,h", "help")
        ("input,i", value<string>(&input_file), "input file")
        ("lower,l", value<float>(&lower_bound_percentage)->default_value(0.0f), "lower bound")
        ("upper,u", value<float>(&upper_bound_percentage)->default_value(1.0f), "upper bound")
        ("keep,k", value<string>(&keep_token)->default_value(""), "keep tokens starting with")
        ;
    variables_map vars;
    store(parse_command_line(argc, argv, opts), vars);
    notify(vars);
    if (vars.count("help") || argc==1) {
        cerr << opts;
        exit(0);
    }
    if (lower_bound_percentage < 0.0 || lower_bound_percentage > 1.0) {
        cerr << "lower bound must be >=0 and <=1" << endl;
        return 2;
    }
    if (upper_bound_percentage < 0.0 || upper_bound_percentage > 1.0) {
        cerr << "upper bound must be >=0 and <=1" << endl;
        return 2;
    }

    // open file
    ifstream file(input_file.c_str());
    if (!file.is_open()) {
        cerr << "couldn't open file [" << input_file << "], sad panda" << endl;
        return -1;
    }

    // make first pass over the file counting the
    // number of documents each token appears in
    string line;
    m_s_ui token_document_freq;
    unsigned int num_docs = 0;
    cerr << "first pass to count tokens..." << endl;
    while (getline(file, line)) {
        // tokenise document
        istringstream iss(line, istringstream::in);
        // ignore primary and secondary id
        iss.ignore(1000, ' ');
        iss.ignore(1000, ' ');
        // collect unique tokens for this document
        s_s tokens;
        copy(istream_iterator<string>(iss),
             istream_iterator<string>(),
             inserter(tokens, tokens.begin()));
        // count tokens
        for (s_s::iterator it=tokens.begin(); it!=tokens.end(); ++it)
            ++token_document_freq[*it];
        // track number docs
        ++num_docs;
    }
    file.close();

    // decide what the limits will be, a token's freq
    // will have to be within this range to be kept
    const unsigned int lower_bound = num_docs * lower_bound_percentage;
    const unsigned int upper_bound = num_docs * upper_bound_percentage;
    cerr << "num_docs=" << num_docs
         << " upper_bound=" << upper_bound
         << " lower_bound=" << lower_bound << endl;

    // decide what tokens to keep
    s_s tokens_to_keep;

    // keep values in range and all "special" ones
    unsigned int num_tokens_to_keep = 0;
    unsigned int num_tokens_to_discard = 0;
    unsigned int num_special_tokens = 0;
    cerr << "first pass to count tokens" << endl;
    const bool have_keep_token = keep_token.length() > 0;
    for(m_s_ui::iterator it=token_document_freq.begin(); it!=token_document_freq.end(); ++it) {
        if (have_keep_token && boost::starts_with(it->first, keep_token)) {
            tokens_to_keep.insert(it->first);
            ++num_special_tokens;
        }
        else if (it->second >= lower_bound && it->second <= upper_bound) {
            tokens_to_keep.insert(it->first);
            ++num_tokens_to_keep;
        }
        else {
            ++num_tokens_to_discard;
        }
    }
    cerr << "num_tokens_to_keep=" << num_tokens_to_keep
         << " num_tokens_to_discard=" << num_tokens_to_discard
         << " num_special_tokens=" << num_special_tokens << endl;

    // make another pass over file, only emitting tokens that we decided to keep
    file.open(input_file.c_str());
    if (!file.is_open()) {
        cerr << "couldn't open file [" << input_file << "] second time?!, extremely sad panda" << endl;
        return -1;
    }

    while (getline(file, line)) {
        // tokenise document in same way
        string token;
        istringstream iss(line, istringstream::in);
        // read and immediately write primary and secondary ids
        iss >> token; cout << token;
        iss >> token; cout << ' ' << token;
        // only emit tokens in keep list
        while(iss >> token)
            if (tokens_to_keep.find(token) != tokens_to_keep.end())
                cout << ' ' << token;
        cout << "\n";
    }

    return 0;
}
