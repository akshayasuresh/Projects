//
//  LorentzVector.cxx
//  defines a class of four vectors, which can then be used to solve problem of general relativity
//
//  Created by Akshaya Suresh on 4/21/14.
//
//

#include "LorentzVector.h"
#include <iostream>
#include <cmath>
#include "ThreeVector.h"

using namespace std;

//default constructor
LorentzVector::LorentzVector() {
    mt = 0;
}

//constructor with arguments
LorentzVector::LorentzVector(const ThreeVector& c, double E)
    : ThreeVector(c), mt(E) {}

LorentzVector::LorentzVector(double E, const ThreeVector& c)
    : ThreeVector(c), mt(E) {}

//copy assignment
LorentzVector::LorentzVector(const LorentzVector& a)
    : ThreeVector(a.x(), a.y(), a.z()), mt(a.t()) {}

//assignment operator
LorentzVector LorentzVector::operator=(const LorentzVector& a){
    if (this!= &a){
        mx=a.mx;
        my=a.my;
        mz=a.mz;
        mt=a.mt;
    }
    return *this;
}

//boolean operators
bool LorentzVector::operator==(const LorentzVector& a) const {
    return (a.mx==a.mx && a.my==a.my && a.mz==a.mz && a.mt==mt);
}

bool LorentzVector::operator!=(const LorentzVector& a) const {
    return !(*this==a);
}

double LorentzVector::t() const{
    return mt;
}

//more member access methods
double LorentzVector::px() const{
    return x();
}

double LorentzVector::py() const{
    return y();
}

double LorentzVector::pz() const{
    return z();
}

double LorentzVector::E() const{
    return mt;
}

ThreeVector LorentzVector::vect() const{
    return ThreeVector(mx,my,mz);
}

//array access
double LorentzVector::operator[](unsigned int l) const {
    switch (l) {
        case 0:
            return mx;
            
        case 1:
            return my;
            
        case 2:
            return mz;
            
        case 3:
            return mt;
            
        default:
            std::cerr << "Invalid index!!!!! :(" << std::endl;
            return 0;
    }
}

//array set
double& LorentzVector::operator[](unsigned int l) {
    switch (l) {
        case 0:
            return mx;
            
        case 1:
            return my;
            
        case 2:
            return mz;
            
        case 3:
            return mt;
            
        default:
            std::cerr << "Invalid index!!!!! :(" << std::endl;
            exit(1);
    }
}

void LorentzVector::setT(double val){
    this->mt=val;
}

//more set member methods
void LorentzVector::setPx(double val){
    setX(val);
}

void LorentzVector::setPy(double val){
    setY(val);
}

void LorentzVector::setPz(double val){
    setZ(val);
}

void LorentzVector::setE(double val){
    this->mt=val;
}

void LorentzVector::setVect(const ThreeVector& c){
    setX(c.x());
    setY(c.y());
    setZ(c.z());
}

//mass and magnitude methods
double LorentzVector::mag() const{
    return sqrt(-mx*mx-my*my-mz*mz+mt*mt);
}

double LorentzVector::mass() const{
    return sqrt(-mx*mx-my*my-mz*mz+mt*mt);
}


//a=b+c
LorentzVector LorentzVector::operator+(const LorentzVector& c){
    ThreeVector threevect(mx+c.mx,my+c.my,mz+c.mz);
    return LorentzVector(threevect, mt+c.mt);
}

//a=b-c
LorentzVector LorentzVector::operator-(const LorentzVector& c){
    ThreeVector threevect(mx-c.mx,my-c.my,mz-c.mz);
    return LorentzVector(threevect,mt-c.mt);
}

//a+=b
LorentzVector LorentzVector::operator+=(const LorentzVector& c){
    mx=mx+c.mx;
    my=my+c.my;
    mz=mz+c.mz;
    mt=mt+c.mt;
    return *this;
}

//a-=b
LorentzVector LorentzVector::operator-=(const LorentzVector& c){
    mx=mx-c.mx;
    my=my-c.my;
    mz=mz-c.mz;
    mt=mt-c.mt;
    return *this;
}

//a=-b
LorentzVector LorentzVector::operator-(){
    ThreeVector threevect(-1.0*mx,-1.0*my,-1.0*mz);
    return LorentzVector(threevect,-mt);
}

//dot product
double LorentzVector::operator*(const LorentzVector& c){
    return mx*c.mx +my*c.my+mz*c.mz + mt*c.mt;
}

//multiplication operator
LorentzVector LorentzVector::operator*(double q) const{
    double a,b,c,d;
    b=mx*q;
    c=my*q;
    d=mz*q;
    ThreeVector threevect(b,c,d);
    a=mt*q;
    return LorentzVector(threevect,a);
}

//c=a/q
LorentzVector LorentzVector::operator/(double q){
    ThreeVector threevect(mx/q, my/q, mz/q);
    return LorentzVector(threevect, mt/q);
}

//multiplication operator
LorentzVector operator*(double q, const LorentzVector& c){
    return c*q;
}

//output operator
std::ostream& operator<<(std::ostream& os, const LorentzVector& c){
    os << c.x() << " "<< c.y() << " " << c.z() << " " << c.t() <<endl;
    return os;
}

//input operator
std::istream& operator<<(std::istream& is, LorentzVector& c){
    double x,y,z,t;
    is >> x >> y >> z >> t;
    c.setX(x);
    c.setY(y);
    c.setZ(z);
    c.setT(t);
    return is;
}

//unit vector 
LorentzVector LorentzVector::unit(){
    ThreeVector a;
    double b,c,d,e;
    c=mx/abs(*this);
    d=my/abs(*this);
    e=my/abs(*this);
    b=mt/abs(*this);
    a=ThreeVector(c,d,e);
    return LorentzVector(a,b);
}

//azimuthal angle
double LorentzVector::phi(){
    ThreeVector threevect(mx,my,mz);
    return threevect.phi();
}

//polar angle
double LorentzVector::theta(){
    ThreeVector threevect(mx,my,mz);
    return threevect.theta();
}

//transverse component
double LorentzVector::perp(){
    ThreeVector threevect(mx,my,mz);
    return threevect.perp();
}

//rotation operators
LorentzVector LorentzVector::rotateX(double alpha){
    ThreeVector threevect(mx,my,mz);
    return LorentzVector(threevect.rotateX(alpha),mt);
}

LorentzVector LorentzVector::rotateY(double alpha){
    ThreeVector threevect(mx,my,mz);
    return LorentzVector(threevect.rotateY(alpha),mt);
}

LorentzVector LorentzVector::rotateZ(double alpha){
    ThreeVector threevect(mx,my,mz);
    return LorentzVector(threevect.rotateZ(alpha),mt);
}

//cross product NOT APPLICABLE FOR FOUR VECTORS, so I've made it private
ThreeVector LorentzVector::cross(const LorentzVector& b){
    ThreeVector threevect(mx,my,mz);
    return threevect.cross(b);
}

//boosts
LorentzVector LorentzVector::boost(const LorentzVector& pfr) const{
    //calculates takes just the momentum part
    ThreeVector vel=pfr.vect();
    //uses the momentum to calculate beta=p/E
    double beta = vel.mag()/pfr.t();
    //uses beta to calculate lambda
    double lam=1.0/(sqrt(1.0-beta*beta));
    double bx, by, bz; //compenents of beta
    bx=vel.x()/pfr.t();
    by=vel.y()/pfr.t();
    bz=vel.z()/pfr.t();
    //the actual boost! (matrix found on wikipedia)
    double t=lam*mt-lam*bx*mx-lam*by*my-lam*bz*mz;
    double x,y,z;
    x=-lam*bx*mt+ (1 + (lam-1)*bx*bx/(beta*beta))*mx + (lam-1)*bx*by/(beta*beta)*my + (lam-1)*bx*bz/(beta*beta)*mz;
    y=-lam*by*mt + (lam-1)*by*bx/(beta*beta)*mx + (1+(lam-1)*by*by/(beta*beta))*my +(lam-1)*by*bz/(beta*beta)*mz;
    z=-lam*bz*mt + (lam-1)*bz*bx/(beta*beta)*mx + (lam-1)*bz*by/(beta*beta)*my + (1 + (lam-1)*bz*bz/(beta*beta))*mz;
    LorentzVector output;
    //sets the four vector to output
    output.setX(x);
    output.setY(y);
    output.setZ(z);
    output.setT(t);
    return output;
}

//absolute value function
double abs(const LorentzVector& c){
    return sqrt(-c.x()*c.x()-c.y()*c.y()-c.z()*c.z()+c.t()*c.t());
}
