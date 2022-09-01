package test;

import java.io.IOException;

import java.util.Map;
import java.util.Scanner;

import org.jsoup.Jsoup;
import org.jsoup.Connection;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

// @author hexated

public class Test {
    
    static Scanner input = new Scanner(System.in);
    static String baseUrl;
    static String userName;
    static String userPass;
        
    public static void main(String[] args) throws IOException {
        try {
            baseUrl = input.nextLine();
            userName = input.nextLine();
            userPass = input.nextLine();
            
            Connection.Response loginForm = Jsoup.connect(baseUrl + "/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess")
                    .data("Database", "10")
                    .data("LogOnDetails.UserName", userName)
                    .data("LogOnDetails.Password", userPass)
                    .method(Connection.Method.POST)
                    .execute();
            
            if (loginForm.body().contains("Your attempt to log in was unsuccessful")){
                System.out.println("incorrect login");
            } else if (loginForm.body().contains("Schedule")){
                Map<String, String> loginCookies = loginForm.cookies();
            
                Document doc = Jsoup.connect(baseUrl + "/HomeAccess/Content/Student/Assignments.aspx")
                    .cookies(loginCookies)
                    .get();
                   
                for (Element table : doc.select("table[id~=plnMain_rptAssigmnetsByCourse_dgCourseAssignments_]")){
                    for (Element row : table.select("tr")){
                    Elements tds = row.select("td");
                    System.out.println(tds.text());
                    
                    }
                    
                }
                
            }    
            
        } catch(IOException e){
            e.printStackTrace();
            System.out.println("invalid url");
            
        }
        
    }
    
}
