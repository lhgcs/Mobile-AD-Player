package com.ad.ad_client;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telecom.TelecomManager;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;
import okhttp3.ResponseBody;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    TextView simpleText = null;
    SensorManager sensorManager = null;
    Sensor sensor = null;
    String IP = null;
    String PORT = null;
    String phoneType = "null";
    String phoneId = "null";

    class Point {
        public float x = 0;
        public float y = 0;
        public float z = 0;
    }

    final float space = 0.1f;
    long lastTime = 0;
    List<Point> pointList = new LinkedList<Point>();

    @SuppressLint("MissingPermission")
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        pointList.add(new Point());
        pointList.add(new Point());
        pointList.add(new Point());

        // 手机
        phoneType = Build.MODEL;
        TelephonyManager manager = (TelephonyManager) (getSystemService(Activity.TELEPHONY_SERVICE));
        if (manager != null) {
            phoneId = manager.getImei(0);
        }

        simpleText = (TextView) findViewById(R.id.sample_text);

        // 服务
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        // 硬件
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        // 注冊
        sensorManager.registerListener(this, sensor, sensorManager.SENSOR_DELAY_NORMAL);
    }

    public void btnclick(View view) {
        String ipStr;
        ipStr = ((EditText) findViewById(R.id.textView_ip)).getText().toString().trim();
        String portStr = ((EditText) findViewById(R.id.textView_port)).getText().toString().trim();

        if (ipStr.equals(null) || portStr.equals(null)) {
            Toast.makeText(this, "null", Toast.LENGTH_LONG).show();
        }

        IP = ipStr;
        PORT = portStr;
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        long temp = System.currentTimeMillis();
        if (temp - lastTime > 1000) {
            lastTime = temp;

            Point p1 = pointList.remove(0); // 删除
            Point p2 = new Point();
            p2.x = event.values[0];
            p2.y = event.values[1];
            p2.z = event.values[2];
            pointList.add(p2);                      // 添加

            simpleText.setText("x:" + p2.x + "\r\ny:" + p2.y + "\r\nz:" + p2.z);
            if (null == IP || null == PORT) {
                Toast.makeText(this, "ip is null", Toast.LENGTH_SHORT).show();
                return;
            }
            // 差异大
            if ((Math.abs(p2.x - p1.x) > space) || (Math.abs(p2.y - p1.y) > space) || (Math.abs(p2.z - p1.z) > space)) {
                boolean res = true;
                for(int i=0; i<2; i++) {
                    Point p = pointList.get(i);
                    if(p.x < -0.009 || p.x > 0.009) {
                        res &=false;
                    }
                    if(p.y < -0.009 || p.y > 0.009) {
                        res &=false;
                    }
                    if(p.z < -0.009 || p.z > 0.009) {
                        res &=false;
                    }
                }
                // 前两次都是0，说明是从开始使用
                if(res) {
                    Toast.makeText(this, "up", Toast.LENGTH_SHORT).show();
                    send_request("up");
                    return;
                }

                res = true;
                for(int i=1; i<3; i++) {
                    Point p = pointList.get(i);
                    if(p.x < -0.009 || p.x > 0.009) {
                        res &=false;
                    }
                    if(p.y < -0.009 || p.y > 0.009) {
                        res &=false;
                    }
                    if(p.z < -0.009 || p.z > 0.009) {
                        res &=false;
                    }
                }
                // 两次都是0，说明是从开始使用
                if(res) {
                    Toast.makeText(this, "down", Toast.LENGTH_SHORT).show();
                    send_request("down");
                }
            }
        }
    }

    public void send_request(String actionType) {
        // 发送请求
        String url = "http://" + IP + ":" + PORT + "/add";
        JSONObject obj = new JSONObject();
        try {
            obj.put("phoneType", phoneType);
            obj.put("phoneId", phoneId);
            obj.put("actionType", actionType);
            //obj.put("time", System.currentTimeMillis());
            DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            obj.put("time", df.format(new Date()));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String json = obj.toString();
        simpleText.setText(json);

        HttpEntity entity = new HttpEntity(url, json, new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                ResponseBody responseBody = response.body();
                final String res = responseBody.string();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        simpleText.setText(res);
                    }
                });
            }
        });
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}
