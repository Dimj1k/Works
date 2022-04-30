#include <fstream>
#include <iostream>
#include <string>
using namespace std;

template < class t >
class Array {
    private:
    t *arr;
    int n, vol;

    void set_Array(int r) {
        if (r >= 0) {
            n = 0; vol = r; arr = new t[vol];
        } else
            throw("Write an Array < type > name(num), where num >= 0 and Integer");
    }

    public:
    Array(int k) {
        set_Array(k);
    }

    int volume() {
        return vol;
    }

    int length() {
        return n;
    }

    t operator [](int index) {
        return arr[index];
    }

    void increase_On(int addvol) {
        if (vol + addvol < n) {
            cout << endl << "increase_On take an argument volume + d(volume) > length arr" << endl;
            return;
        }
        vol += addvol;
        delete addvol;
        set_volume(vol);
            
    }

    void increase_In(int mulvol) {
        if (mulvol <= 1) { cout << endl << "increase_In take an argument > 1" << endl; return; }
        vol *= mulvol;
        delete mulvol;
        set_volume(vol);
    }

    void set_volume(int newvol) {
        if (newvol < n) { cout << endl << "set_volume take an argument newvolume > length arr"; return; }
        vol = newvol;
        t *tmp = arr;
        arr = new t[vol];
        for (int i = 0; i < n; i++)
            arr[i] = tmp[i];
        return;
    }

    void append(t el) {
        if (n == vol) { cout << endl << "\nIncrease array. For append: " << el << endl; return; }
        arr[n] = el;
        n++;
    }

    void operator +(t el) {
        append(el);
    }

    void remove(t el, int num = 1) {
        if (num < 1) { return; } 
        int removed = 0;
        t *tmp = arr;
        arr = new t[vol];
        for (int i = 0; i < n; i++) {
            if (tmp[i] == el && removed != num) { removed++; continue; }
            arr[i - removed] = tmp[i];
        }
        n -= removed;
        return;
    }

    void print() {
        cout << "[";
        if (n > 0)
            cout << arr[0];
        for (int i = 1; i < n; i++)
            cout << ", " << arr[i];
        cout << "]\n";
    }
};

int max2(int *a) {
    if (a[0] > a[1]) 
        return a[0];
    return a[1];
}

int min2(int *a) {
    if (a[0] > a[1])
        return a[1];
    return a[0];
}

int max(Array < int > das) {
    int max = -1;
    for (int i = 0; i < das.length(); i++){
        if (das[i] > max) max = das[i];
    }
    return max;
}

int min(Array < int > das) {
    int min = 10001;
    for (int i = 0; i < das.length(); i++){
        if (das[i] < min) min = das[i];
    }
    return min;
}

int main() {
    Array < int > a(30110); Array < int > b(30110);
    long long ans1 = 0, ans2 = 0;
    int values[2], mini, maxi;
    ifstream f("4.txt");
    string line;
    while (getline(f, line)) {
        values[0] = stoi(line.substr(0, line.find(' ')));
        if (values[0] % 2 != 0) {
            values[1] = stoi(line.substr(line.find(' ')));
            a + max2(values); b + min2(values);
        }
    }
    f.close();
    for (int i = 0; i < a.length(); i++) {
        ans1 += a[i]; ans2 += b[i];
    }
    while (ans1 % 2 != 0) {
        mini = min(a);
        ans1 -= mini; a.remove(mini);
    }
    while (ans2 % 2 == 0) {
        maxi = max(a);
        ans2 -= maxi; a.remove(maxi);
    }
    cout << "Sum of maximum numbers: " << ans1 << "\nSum of minimum numbers: " << ans2 << endl;
}
