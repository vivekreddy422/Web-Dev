/******************************************************************************

                            Online Java Compiler.
                Code, Compile, Run and Debug java program online.
Write your code in this editor and press "Run" button to execute it.

*******************************************************************************/
import java.util.*;
class NumberString implements Comparable<NumberString>{
    String x;
    public NumberString(String x) {
        char[] ch = x.toCharArray();
        int i = 0;
        for (; i < ch.length; i++) {
            if (ch[i] != '0') {
                break;
            }
        }
        String temp = "";
        for(int j = i; j < ch.length; j++) {
            temp += ch[j];
        }
        this.x = temp;
    }
    public int compareTo(NumberString that) {
        if (this.x.length() < that.x.length()) {
            return -1;
        } else if (this.x.length() > that.x.length()) {
            return 1;
        } else {
            return this.x.compareTo(that.x);
        }
    }
    
    public String toString() {
        return this.x;
    }
}
public class Main
{
	public static void main(String[] args) {
		System.out.println("Hello World");
		NumberString[] numStrings = new NumberString[2];
		numStrings[0] = new NumberString("12345");
		numStrings[1] = new NumberString("1234");
		Arrays.sort(numStrings);
		System.out.println(Arrays.toString(numStrings));
	}
}
