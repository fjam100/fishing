#include <iostream>
#include <sstream>
#include <stdio.h>
using namespace std;

int
main()
{
  FILE *file;
  //Opening device file

  int getnum;

  while (true)
    {
        file = fopen("/dev/ttyACM0", "w");
        string msg="255, 255, 25, 102, 101, 221, 113, 0, 0, 50";
        //std::string msg = "00 00 00 00 00 06 01 05 00 FF 00 00";

        std::istringstream buffer(msg);

        char bbuffer[10];

        unsigned int ch;
        for (int i=0; buffer >> std::hex >> ch; i++)
            bbuffer[i] = ch & 0xff;

        /*cout << ">>" << endl;
        cin >> getnum; */
        fwrite(bbuffer,1,10,file); //Writing to the file*/
        fclose(file);
    }

}

