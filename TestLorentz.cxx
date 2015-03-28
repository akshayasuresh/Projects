//
//  TestLorentz.cxx
//  
//
//  Created by Akshaya Suresh on 4/24/14.
//
//

#include <iostream>
#include <cmath>
#include "ThreeVector.h"
#include "LorentzVector.h"
#include <cstdlib>


using namespace std;

int main(){
    int N;
    double px;
    double py;
    double pz;
    double eP, eE, pP, pE;
    LorentzVector J,e,pos, E, P;
    ThreeVector p;
    double Energy;
    double ranphi;
    double rancos;
    double pi = acos(-1);
	long seed;
    
    
    //user defines the momentum of the mother particle as well as the number of desired decays
    cout << "Number of Decays?" <<endl;
    cin>>N;
    cout << "Momentum in X?" <<endl;
    cin>>px;
    cout << "Momentum in Y?" <<endl;
    cin>>py;
    cout << "Momentum in Z?" <<endl;
    cin>>pz;
    p.setX(px);
    p.setY(py);
    p.setZ(pz);
    //calculate the energy of the mother particle using E^2=m^2 + |p|^2
    Energy=sqrt(3.096*3.096+abs(p)*abs(p));
    J.setT(Energy);
    J.setVect(p);
    
    //initialize random number generator
    cout << "Enter a seed: " << endl;
	cin >> seed;
	srand48(seed);
    //sets up the loop for the correct number of decays
    for (int i=0; i<(N); i++){
        //gives the energy for the two daughter particles
        eE=3.096/2;
        pE=eE;
        //gives the momentum magnitude for the daughters using E^2=m^2 + |p|^2
        eP=sqrt(eE*eE-0.0005109*0.0005109);
        //generates random emission angles
        rancos=drand48()*2-1;
        ranphi=drand48()*2*pi;
        //finds the momentum components
        e.setX(eP*sin(acos(rancos))*cos(ranphi));
        e.setY(eP*sin(ranphi)*sqrt(1-rancos*rancos));
        e.setZ(rancos*eP);
        pos.setX(-e.x());
        pos.setY(-e.y());
        pos.setZ(-e.z());
        e.setT(eE);
        pos.setT(pE);
        //boosts the daughter four vectors
        E=e.boost(J);
        P=pos.boost(J);
        cout << E;
        cout << P;
        cout << " " <<endl;
    }
    //tests for invariance
    //electron mass=positron mass=0.0005109
    cout << "Mass matches rest mass: " << E.mass() << " " <<P.mass()<<endl;
    //invariant mass is indeed, invariant
    cout << "Invariant mass: "<< abs(E.vect()+P.vect()) << " " << abs(J.vect())<<endl;
    //energy conservation
    cout << "Energy conservation " << (E.t()+P.t()) << " " << J.t()<<endl;
    
    return 0;
