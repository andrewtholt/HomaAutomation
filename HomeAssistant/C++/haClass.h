#include <string>
#include <map>
#include <vector>


class haClass {
    private:
        int mqttKeepAlive = 20;
        bool mqttSetCleanSession=true;

        std::string clientId;

        std::string serverAddress="127.0.0.1";

        bool connected=false;

        std::map<std::string,std::string> subList;

        std::string logicToState(bool flag);
        bool stateToLogic(std::string state);
    public:
        haClass(std::string cfgFile, std::string clientId);
};
