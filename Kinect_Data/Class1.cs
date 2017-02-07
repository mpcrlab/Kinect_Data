using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RGiesecke.DllExport;
using System.Runtime.InteropServices;

namespace Kinect_Data
{
    public class Class1
    {
        [DllExport("add", CallingConvention = CallingConvention.Cdecl)]
        public static int Add(int left, int right)
        {
            return left + right;
        }
    }
}
