#include <iostream>
#include <cmath>
#include <cstdlib>
#include <vector>

class point {
protected:
    double x;
    double y;
    int index;
public:
    point();

    void setX(double X) { x = X; }

    void setY(double Y) { y = Y; }

    double getX() { return x; }

    double getY() { return y; }
};

point::point() {
    x = 0;
    y = 0;
    index = 0;
}

class crane : public point {

public:
    crane(double X, double Y, int INDEX);
//    double getX (){ return x;}
//    double getY (){ return y;}
};

crane::crane(double X, double Y, int INDEX) {
    x = X;
    y = Y;
    index = INDEX;
    std::cout << "Crane " << index << " added to testbed | Coordinates: X = " << getX() << " Y = " << getY() << "\n";
}

class hook : public point {
protected:
    int index;
    double z;
    double r;
    double theta;
public:
    hook(double X, double Y, double Z, double R, double THETA, int INDEX);

    void setR(double R) { r = R; }

    void setZ(double Z) { z = Z; }

    void setTheta(double THETA) { theta = THETA * M_PI / 360; }

    void setX(double X, double R, double theta) { x = X + R * cos(theta); }

    void setY(double Y, double R, double theta) { y = Y + R * sin(theta); }

//    double getX(){return x;}
//    double getY(){return y;}
    double getZ() { return z; }

    double getR() { return r; }

    double getTheta() { return theta; }

};

hook::hook(double X, double Y, double R, double Z, double THETA, int INDEX) {
    z = Z;
    r = R;
    theta = THETA;
    index = INDEX;
    std::cout << "Hook " << index << " added to crane " << index << " Coordinates: Theta = " << getTheta() << " R = "
              << getR() << " Z = " << getZ();
}

std::vector<hook> initializeHooks(std::vector<crane> cranes) {
    std::vector<hook> newHooks;
    std::vector<double> inputFromCranes{0.3, 1.5, 120, 0.6, 1.2, 35, 0.5, 1.0, 48, 0.24, 0.8, 273};
    int inputIterator = 0;
    for (int i = 0; i < cranes.size(); i++) {
        hook tmpHook(0, 0, inputFromCranes[inputIterator], inputFromCranes[inputIterator + 1],
                     inputFromCranes[inputIterator + 2], i + 1);
        tmpHook.setX(cranes[i].getX(), tmpHook.getR(), tmpHook.getTheta());
        tmpHook.setY(cranes[i].getY(), tmpHook.getR(), tmpHook.getTheta());
        std::cout << " X = " << tmpHook.getX() << " Y = " << tmpHook.getY() << "\n";
        newHooks.push_back(tmpHook);
        inputIterator += 3;
    }
    return newHooks;

};

int main(int argc, char **argv) {
//    std::cout << "Hello, World!" << std::endl;
//    std::cout<<argc;
    auto craneNumber = atoi(argv[1]);
    double craneCoordinates[argc - 1];
    int index = 1;

    std::vector<crane> activeCranes;
    std::vector<hook> activeHooks;

    for (int i = 0; i < argc - 2; i++) {
        craneCoordinates[i] = strtod(argv[i + 2], nullptr);
    }
    for (auto i = 0; i < craneNumber * 2; i += 2) {
//        std::cout<<argv[argc];
        crane tmpCrane(craneCoordinates[i], craneCoordinates[i + 1], index);
        activeCranes.push_back(tmpCrane);
//   std::cout<<craneCoordinates[i]<<" | ";
        index++;
    }

    activeHooks = initializeHooks(activeCranes);

    std::cout << activeCranes.size();


    return 0;
}