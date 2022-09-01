package com.example.hacaccess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.github.florent37.viewtooltip.ViewTooltip;

import org.jsoup.Jsoup;
import org.jsoup.Connection;

import java.io.IOException;


public class MainActivity extends AppCompatActivity {

    EditText userName;
    EditText userPass;
    EditText hacAddress;
    Button loginButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        userName = findViewById(R.id.editTextUserName);
        userPass = findViewById(R.id.editTextUserPass);
        hacAddress = findViewById(R.id.editTextHacAddress);
        loginButton = findViewById(R.id.btnLogin);

        hacAddress.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    ViewTooltip
                            .on(MainActivity.this, hacAddress)
                            .autoHide(true, 2000)
                            .corner(30)
                            .position(ViewTooltip.Position.TOP)
                            .text("ex. https://hac.friscoisd.org/")
                            .show();
                }

            }
        });

        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                login(hacAddress.getText().toString(), userName.getText().toString(), userPass.getText().toString());
            }
        });

    }

    private void login(String baseUrl, String user, String pass) {
        try {
            Connection.Response loginForm = Jsoup.connect(baseUrl + "/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess")
                    .data("Database", "10")
                    .data("LogOnDetails.UserName", user)
                    .data("LogOnDetails.Password", pass)
                    .method(Connection.Method.POST)
                    .execute();

            if (loginForm.body().contains("Your attempt to log in was unsuccessful")) {
                makeToast("Invalid Login Credentials.");
            } else if (loginForm.body().contains("Schedule")){
                makeToast("Loading, Please wait...");

                Intent intent = new Intent(MainActivity.this, NavigationActivity.class);
                intent.putExtra("url", baseUrl);
                intent.putExtra("name", user);
                intent.putExtra("password", pass);

                startActivity(intent);
            }

        } catch (IOException e) {
            e.printStackTrace();
            makeToast("Invalid URL.");

        }
    }

    private void makeToast(String msg){
        Toast t = Toast.makeText(MainActivity.this,
                msg, Toast.LENGTH_LONG);
        t.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 200);
        t.show();
    }
}