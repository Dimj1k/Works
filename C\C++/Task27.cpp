#include <fstream>
#include <iostream>
using namespace std;

class Arrayint {
    private:
    int *arr;
    int n, vol;
    float incrin = 1.1;

    void set_Array(int r) {
        if (r >= 0) {
            n = 0; vol = r; arr = new int[vol];
        } else
            throw("Write an Array < type > name(num), where num >= 0 and Integer");
    }

    public:
    Arrayint(int k) {
        set_Array(k);
    }

    ~Arrayint() {
        delete []arr;
    }

    int volume() {
        return vol;
    }

    int length() {
        return n;
    }

    int operator [](int index) {
        return arr[index];
    }

    void increase_On(int addvol) {
        if (vol + addvol < n) {
            cout << endl << "increase_On take an argument volume + d(volume) > length arr" << endl;
            return;
        }
        vol += addvol;
        set_volume(vol);
            
    }

    void increase_In(int mulvol) {
        if (mulvol <= 1) { cout << endl << "increase_In take an argument > 1" << endl; return; }
        vol *= mulvol;
        set_volume(vol);
    }

    void set_volume(int newvol) {
        if (newvol < n) { cout << endl << "set_volume take an argument newvolume > length arr"; return; }
        vol = newvol;
        int *tmp = arr;
        arr = new int[vol];
        for (int i = 0; i < n; i++)
            arr[i] = tmp[i];
        return;
    }

    void set_incrin(float num) {
        if (num < 1) { cout << endl << "set_incrin take an argument > 1"; return; }
        incrin = num;
    }

    void append(int el) {
        if (n == vol)
            set_volume(vol * incrin);
        arr[n] = el;
        n++;
    }

    void operator +(int el) {
        append(el);
    }

    void remove(int el, int num = 1) {
        if (num < 1) { return; } 
        int removed = 0;
        int *tmp = arr;
        arr = new int[vol];
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

class MyStringWithSplit : public string {
    // public:
    // string *split(char splitter = '\n', int items = 10) {
    //     string *spliten = new string[items];
    //     int j = 0;
    //     for (int i = 0; i < strlen(basic_string); i++) {
    //         if (basic_string[i] != splitter)
    //             spliten[j] = basic_string[i];
    //         else
    //             j++;
    //     }
    //     return spliten;
    // }
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

int max(Arrayint das) {
    int max = -1;
    for (int i = 0; i < das.length(); i++){
        if (das[i] > max) max = das[i];
    }
    return max;
}

int min(Arrayint das) {
    int min = 10001;
    for (int i = 0; i < das.length(); i++){
        if (das[i] < min) min = das[i];
    }
    return min;
}

int main() {
    Arrayint a(30110); Arrayint b(30110);
    long long ans1 = 0, ans2 = 0;
    int values[2], mini, maxi;
    ifstream f("4.txt");
    MyStringWithSplit line;
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
    if (ans1 % 2 != 0) {
        mini = min(a);
        ans1 -= mini; a.remove(mini);
    }
    if (ans2 % 2 == 0) {
        maxi = max(b);
        ans2 -= maxi; b.remove(maxi);
    }
    cout << "Sum of maximum numbers: " << ans1 << "\nSum of minimum numbers: " << ans2 << endl;
}
