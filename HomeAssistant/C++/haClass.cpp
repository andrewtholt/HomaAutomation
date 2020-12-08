/***********************************************************************
 * AUTHOR: andrewh <andrewh>
 *   FILE: .//haClass.cpp
 *   DATE: Mon Sep 30 17:17:56 2019
 *  DESCR: 
 ***********************************************************************/
#include "haClass.h"

/***********************************************************************
 *  Method: haClass::logicToState
 *  Params: bool flag
 * Returns: std::string
 * Effects: 
 ***********************************************************************/
std::string haClass::logicToState(bool flag) {

    std::string res;

    if (flag) {
        res="TRUE";
    } else {
        res="FALSE";
    }
    return res;
}


/***********************************************************************
 *  Method: haClass::stateToLogic
 *  Params: std::string state
 * Returns: bool
 * Effects: 
 ***********************************************************************/
bool haClass::stateToLogic(std::string state) {

    bool logicState=false;

    std::vector<std::string> logicTrue{"ON","TRUE","YES"};
    std::vector<std::string> logicFalse{"OFF","FALSE","NO"};

    if ( std::find(logicTrue.begin(), logicTrue.end(), state) != logicTrue.end()) {
        logicState = true;
    }

    return logicState;
}


/***********************************************************************
 *  Method: haClass::haClass
 *  Params: string cfgFile, string clientId
 * Effects: 
 ***********************************************************************/
haClass::haClass(std::string cfgFile, std::string clientId)
{
}


