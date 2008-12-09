#include <algorithm>
#include <cassert>
#include <cctype>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::fixed;
using std::getline;
using std::istream;
using std::istringstream;
using std::make_pair;
using std::map;
using std::min;
using std::pair;
using std::setprecision;
using std::sqrt;
using std::string;
using std::vector;

istringstream& read_line(istream& in, istringstream& line)
{
    string str;
    getline(in, str);
    line.clear();
    line.str(str);
    return line;
}

string strip(const string& str)
{
    string::const_iterator first = str.begin();
    string::const_iterator last = str.end();
    while (first != last && isspace(*first)) {
        ++first;
    }
    while (first != last && isspace(*(last - 1))) {
        --last;
    }
    return string(first, last);
}

struct context_type {
    typedef vector<double> gas_cost_vector;
    typedef pair<int, int> position_type;
    typedef vector<int> price_list_type;
    typedef vector<double> min_cost_vector;

    int item_count;
    int store_count;
    int gas_price;
    vector<string> item_names;
    int perishables; 
    vector<gas_cost_vector> gas_costs;
    vector<position_type> positions;
    vector<price_list_type> price_lists;
    vector<int> inventories;
    vector<min_cost_vector> min_costs;

    context_type()
        : item_count(0), store_count(0), gas_price(0), perishables(0)
    { }
};

int parse_case_count(istream& in)
{
    istringstream line;
    int case_count = 0;
    read_line(in, line) >> case_count;
    return case_count;
}

void parse_case_args(istream& in, context_type& context)
{
    istringstream line;
    read_line(in, line) >> context.item_count >> context.store_count
                        >> context.gas_price;
}

void parse_items(istream& in, context_type& context)
{
    istringstream line;
    read_line(in, line);
    for (int item = 0; item < context.item_count; ++item) {
        string item_arg;
        line >> item_arg;
        item_arg = strip(item_arg);
        if (item_arg[item_arg.size() - 1] == '!') {
            item_arg.resize(item_arg.size() - 1);
            context.perishables |= 1 << item;
        }
        context.item_names.push_back(item_arg);
    }
}

void parse_stores(istream& in, context_type& context)
{
    istringstream line;
    for (int store = 0; store < context.store_count; ++store) {
        int x = 0, y = 0;
        map<string, int> prices;
        context_type::price_list_type price_list(context.item_count, -1);
        int inventory = 0;
        read_line(in, line);
        line >> x >> y;
        for (;;) {
            string item_name;
            int price = -1;
            getline(line, item_name, ':');
            item_name = strip(item_name);
            line >> price;
            if (price == -1) {
                break;
            }
            prices[item_name] = price;
        }
        for (int item = 0; item < context.item_count; ++item) {
            map<string, int>::iterator found
                = prices.find(context.item_names[item]);
            if (found != prices.end()) {
                price_list[item] = found->second;
                inventory |= 1 << item;
            }
        }
        context.positions.push_back(make_pair(x, y));
        context.price_lists.push_back(price_list);
        context.inventories.push_back(inventory);            
    }
}

void parse_case(istream& in, context_type& context)
{
    parse_case_args(in, context);
    parse_items(in, context);
    parse_stores(in, context);
}

void precalc_gas_costs(context_type& context)
{
    for (int store = 0; store <= context.store_count; ++store) {
        context.gas_costs.resize(context.gas_costs.size() + 1);
        int store_x = context.positions[store].first;
        int store_y = context.positions[store].second;
        for (int dest = 0; dest <= context.store_count; ++dest) {
            int dest_x = context.positions[dest].first;
            int dest_y = context.positions[dest].second;
            int dx = dest_x - store_x, dy = dest_y - store_y;
            double dist = sqrt(double(dx * dx + dy * dy));
            context.gas_costs[store].push_back(context.gas_price * dist);
        }
    }
}

void prealloc_min_costs(context_type& context)
{
    typedef context_type::min_cost_vector min_cost_vector;
    context.min_costs.resize(2 * (context.store_count + 1),
                             min_cost_vector(1 << context.item_count, -1));
}

double min_cost(int store, int items, bool perishing, context_type& context);

double calc_min_cost(int store, int items, bool perishing,
                     context_type& context)
{
    if (!items) {
        // We are done shopping.
        return context.gas_costs[store][context.store_count];
    } else if (perishing) {
        // Return to the house...
        double result = context.gas_costs[store][context.store_count]
            + min_cost(context.store_count, items, false, context);

        // ...or buy something more here.
        if (int inventory = items & context.inventories[store]) {
            for (int item = 0; item < context.item_count; ++item) {
                if (inventory & (1 << item)) {
                    double cost = context.price_lists[store][item]
                        + min_cost(store, items & ~(1 << item), true, context);
                    result = min(cost, result);
                }
            }
        }
        return result;
    } else {
        // Buy something at a store.
        double result = -1;
        for (int dest = 0; dest < context.store_count; ++dest) {
            if (int inventory = items & context.inventories[dest]) {
                for (int item = 0; item < context.item_count; ++item) {
                    if (inventory & (1 << item)) {
                        double cost = context.gas_costs[store][dest]
                            + context.price_lists[dest][item]
                            + min_cost(dest, items & ~(1 << item),
                                       bool(context.perishables & (1 << item)),
                                       context);
                        if (result < 0 || cost < result) {
                            result = cost;
                        }
                    }
                }
            }
        }
        assert(result >= 0);
        return result;
    }
}

double min_cost(int store, int items, bool perishing, context_type& context)
{
    int key = store << 1 | perishing;
    double result = context.min_costs[key][items];
    if (result < 0) {
        result = calc_min_cost(store, items, perishing, context);
        context.min_costs[key][items] = result;
    }
    return result;
}

double min_cost(context_type& context)
{
    return min_cost(context.store_count, (1 << context.item_count) - 1, false,
                    context);
}

int main()
{
    cout << fixed << setprecision(7);
    int case_count = parse_case_count(cin);
    for (int case_ = 0; case_ < case_count; ++case_) {
        context_type context;
        parse_case(cin, context);
        context.positions.push_back(make_pair(0, 0));
        precalc_gas_costs(context);
        prealloc_min_costs(context);
        cout << "Case #" << case_ + 1 << ": " << min_cost(context) << endl;
    }
    return 0;
}
