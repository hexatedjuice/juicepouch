package com.example.hacaccess;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentTransaction;

import android.os.Bundle;
import android.os.StrictMode;
import android.widget.Button;
import android.widget.LinearLayout;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.Map;


public class NavigationActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        Bundle bundle = getIntent().getExtras();
        String baseUrl = bundle.getString("url");
        String userName = bundle.getString("name");
        String userPass = bundle.getString("password");

        try {
            Connection.Response loginForm = Jsoup.connect(baseUrl + "/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess")
                    .data("Database", "10")
                    .data("LogOnDetails.UserName", userName)
                    .data("LogOnDetails.Password", userPass)
                    .method(Connection.Method.POST)
                    .execute();

            Map<String, String> loginCookies = loginForm.cookies();

            Document doc = Jsoup.connect(baseUrl + "/HomeAccess/Content/Student/Assignments.aspx")
                    .cookies(loginCookies)
                    .get();

//            for (Element table : doc.select("table[id~=plnMain_rptAssigmnetsByCourse_dgCourseAssignments_]")) {
//                for (Element row : table.select("tr")) {
//                    Elements tds = row.select("td");
//                    System.out.println(tds.text());
//                }
//            }
//
            // get classes to create buttons
            Elements classes = doc.select("a[class=sg-header-heading]");
            for (Element className : classes){
                createButton(className.text());
            }

//            FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
//            ft.replace(R.id.flfragment, new navFragment());
//            ft.commit();


        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void createButton(String name){
        Button myButton = new Button(NavigationActivity.this);
        myButton.setText(name);
//        myButton.setId(name);

        LinearLayout ll = (LinearLayout)findViewById(R.id.activity_navigation);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        ll.addView(myButton, lp);
    }


}