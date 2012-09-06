import java.util.Stack;
import java.lang.annotation.*;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;

@Target(TYPE)
@Retention(RUNTIME)

@interface Author {
  public String name() default  "John Snow" ;
  public String uteid() default  "js123" ;
}


//TODO(EE422C): implement this as specified in the lab
class StackLeftoverException extends RuntimeException {

}

@Author(name="John Snow", uteid="js123")
public class Postfix {
    
  //TODO(EE422C): implement this function as per the lab specification
  public static int evalPostfix( String s ) throws 

  }

  // this is a convenience function; it's a little
  // easier to experiment with the calculator without junit
  // using the main within the class, specified below
  public static void testEvalPostfix( String s ) {
    try {
      Integer result = evalPostfix( s );
      System.out.println(s + " = " + result );
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static void main(String args[]) {
    testEvalPostfix( "1 3 + 0 /" );
    testEvalPostfix( " 2    -7    + -6    * -1 /  ");
    testEvalPostfix( "1 2 +" );
    testEvalPostfix( "1 2 + 3 *" );
    testEvalPostfix( "1 2 + 3 * +" );
    testEvalPostfix( " 0 1 2 + 3 * +" );
    testEvalPostfix( " 0 1 2 + 3 * + -123" );
    testEvalPostfix( "+" );
    testEvalPostfix( "a b +" );
    testEvalPostfix( "12.3 44 +" );
  }
}