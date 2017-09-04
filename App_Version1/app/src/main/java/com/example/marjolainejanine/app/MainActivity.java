package com.example.marjolainejanine.app;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class MainActivity extends AppCompatActivity implements SensorEventListener {
    Button peakDetection;
    Button save;
    Button display;
    String val;
    String valx,valy,valz,valxC,valyC,valzC;
    float[] valT= new float[3];
    double[] valG= new double[3];
    float g;
    /*********************************************************************/
    /**GPS attributes***********************************************/
    /*********************************************************************/
    double latitude=0;
    double longitude=0;
    double latP[] = new double[60000];
    double longiP[] = new double[60000];
    TextView la;
    TextView lon;

    /********************************************************************/
    /** light Sensor attributes***********************************************/
    /*********************************************************************/

    // Light current value
    float l = 0;

    // Sensor manager
    SensorManager sensorManager;

    //light sensor
    Sensor light;

    //light data display
    TextView lin;
    int cpt = 0; // compteur


    float lux[] = new float[60000];

    /*********************************************************************/
    /** accelerometer Sensor attributes***********************************************/
    /*********************************************************************/

    Sensor accelerometer;
    float x = 0, y = 0, z = 0;
    float accex[] = new float[60000];
    float accey[] = new float[60000];
    float accez[] = new float[60000];
    TextView xin, yin, zin;



    /*************************************************************/
    /**Compass *****************************************************************/
    /*********************************************************/

    //Orientation calculation

    float xCompass = 0, yCompass = 0, zCompass = 0;
    Sensor magnetic;
    float[] accelerometerVector = new float[3];
    float[] magneticVector = new float[3];
    float[] resultMatrix = new float[9];
    float[] values = new float[3];
    TextView xinComp, yinComp, zinComp;
    float xComp[] = new float[60000];
    float yComp[] = new float[60000];
    float zComp[] = new float[60000];
    int active=0;

    /*************************************************************/
    /**send email *****************************************************************/
    /*********************************************************/
    Button send;
    TextView text;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // HMI

        //ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);


        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);// SensorManager declaration
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE); //locationManager declaration


        save = (Button) findViewById(R.id.save); //Saving button
        display = (Button) findViewById(R.id.display); //Display button
        send = (Button) findViewById(R.id.send); // Send by mail button

        text = (TextView) findViewById(R.id.text);
        text.setVisibility(View.INVISIBLE);

        /**************************************
         *GPS
         * *****************************/

        //gps system

        //Entrées "in" et sorties "out" des données
        la = (TextView) findViewById(R.id.la);
        lon = (TextView) findViewById(R.id.lon);


        //GPS Permission

        //Provider requirements
        Criteria criteria = new Criteria();
        criteria.setAccuracy(Criteria.ACCURACY_FINE);
        criteria.setAltitudeRequired(true);
        criteria.setBearingRequired(false);
        criteria.setCostAllowed(false);
        criteria.setPowerRequirement(Criteria.POWER_MEDIUM);
        criteria.setSpeedRequired(true);


        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }

        locationManager.requestLocationUpdates(locationManager.getBestProvider(criteria, true), 0, 0, gpsListener);


        /**************************************
         * light sensor
         * *****************************/

        light = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);// Light sensor instantiation

        //Entrées "in" et sorties "out" des données
        lin = (TextView) findViewById(R.id.lin);


        /**************************************
         * accelerometer sensor
         * *****************************/

        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER); //accelerometer sensor instantiation
        //Entrées "in" et sorties "out" des données
        xin = (TextView) findViewById(R.id.xin);
        yin = (TextView) findViewById(R.id.yin);
        zin = (TextView) findViewById(R.id.zin);


        /******************************************
         * magnetic sensor
         **************************************/
        magnetic = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD); //magnetic sensor instantiation

        //Entrées "in" et sorties "out" des données
        xinComp = (TextView) findViewById(R.id.xinComp);
        yinComp = (TextView) findViewById(R.id.yinComp);
        zinComp = (TextView) findViewById(R.id.zinComp);


        /***************************************************************/
        /**Register ************************************/
        /***************************************************************/

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                active = 1;

                lRegister("/App/lightdata.txt");
                xRegister("/App/xdata.txt");
                yRegister("/App/ydata.txt");
                zRegister("/App/zdata.txt");
                xcompRegister("/App/xCompdata.txt");
                ycompRegister("/App/yCompdata.txt");
                zcompRegister("/App/zCompdata.txt");
                latRegister("/App/latdata.txt");

                lonRegister("/App/longidata.txt");

                //Afficher le nombre d'éléments enregistrés à l'appui sur le bouton save
                Toast.makeText(getApplicationContext(), "Enregistrement terminé avec " + String.valueOf(cpt) + " données ", Toast.LENGTH_LONG).show();


            }

        });

        /***************************************************************/
        /**display ************************************/
        /***************************************************************/
        display.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                lDisplay("/App/lightdata.txt");
                lDisplay("/App/xdata.txt");
                lDisplay("/App/ydata.txt");
                lDisplay("/App/zdata.txt");
                lDisplay("/App/xCompdata.txt");
                lDisplay("/App/yCompdata.txt");
                lDisplay("/App/zCompdata.txt");
                lDisplay("/App/latdata.txt");
                lDisplay("/App/longidata.txt");

            }

        });

        /***************************************************************/
        /**send email ************************************/
        /***************************************************************/
        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {  //click on the button save
                sendEmail();
            }

        });

        peakDetection = (Button) findViewById(R.id.peakDetection);

        peakDetection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(MainActivity.this, PeakDetection.class);
                startActivity(intent);

            }
        });

    }

    /***************************************************************/
    /**CALL the listener of GPS  ************************************/
    /***************************************************************/
    // Call the listener of the gps
    LocationListener gpsListener = new LocationListener() {
        @Override
        public void onLocationChanged(Location location) {

            if (location!=null) {

                //get the latitude
               latitude = location.getLatitude();

                // get the longitude
                longitude = location.getLongitude();
            }
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {}

        @Override
        public void onProviderDisabled(String provider) {}

        @Override
        public void onProviderEnabled(String provider) {}

    };

    @Override
    protected void onPause() {
        //unregister sensor listener
        sensorManager.unregisterListener((SensorEventListener) this, light);
        sensorManager.unregisterListener((SensorEventListener) this, accelerometer);
        sensorManager.unregisterListener((SensorEventListener) this, magnetic);

        super.onPause();
    }

    @Override
    protected void onResume() {
        // register sensor listener
        sensorManager.registerListener((SensorEventListener) this, light, SensorManager.SENSOR_DELAY_GAME);
        sensorManager.registerListener((SensorEventListener) this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
        sensorManager.registerListener((SensorEventListener) this, magnetic, SensorManager.SENSOR_DELAY_GAME);
        super.onResume();
    }


    /*****************************************************************/
    /** SensorEventListener ******************************************/
    /*****************************************************************/

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        // Update

        /*****************************
         * light sensor************************
         ********************************/
        if (event.sensor.getType() == Sensor.TYPE_LIGHT) {
            // light value
            l = event.values[0];

        }
        //light value storage

        // Fonction enregistrer
        //


        /*****************************
         * accelerometer sensor************************
         ********************************/

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            x = event.values[0];
            y = event.values[1];
            z = event.values[2];



            if (active==0) {
                // enregistrer

                lux[cpt] = l;
                // Conversion and put of x,y,z values on the interface
                String liValue = String.valueOf(l);
                lin.setText(liValue);

                // Accelerometer values storage
                accex[cpt] = x;
                accey[cpt] = y;
                accez[cpt] = z;
                //Conversion and put of x,y,z values on the interface
                String xValue = String.valueOf(x);
                xin.setText(xValue);
                String yValue = String.valueOf(y);
                yin.setText(yValue);
                String zValue = String.valueOf(z);
                zin.setText(zValue);


                //Compass values storage
                xComp[cpt] = xCompass;
                yComp[cpt] = yCompass;
                zComp[cpt] = zCompass;
                //Conversion and put of x,y,z values on the interface
                String xCompValue = String.valueOf(xCompass);
                xinComp.setText(xCompValue);
                String yCompValue = String.valueOf(yCompass);
                yinComp.setText(yCompValue);
                String zCompValue = String.valueOf(zCompass);
                zinComp.setText(zCompValue);

                //GPS values storage
                latP[cpt] = latitude;
                longiP[cpt] = longitude;
                //Conversion and put of latitude & longitude values on the interface
                String latitudeValue = String.valueOf(latitude);
                la.setText(latitudeValue);
                String longitudeValue = String.valueOf(longitude);
                lon.setText(longitudeValue);

                cpt = cpt + 1;
            }




        }

        /*****************************
         * compass************************
         ********************************/
        // Mettre à jour la valeur de l'accéléromètre et du champ magnétique
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            accelerometerVector = event.values;
        } else if (event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD) {
            magneticVector = event.values;
        }

        // Rotation Matrix
        SensorManager.getRotationMatrix(resultMatrix, null, accelerometerVector, magneticVector);

        // Orientation vector related with rotation Matrix
        SensorManager.getOrientation(resultMatrix, values);

        /** The Azimuth
         * x= 0 when y axis point out magnetic north; x=180 when yaxis point out magnetic south
         * x=90 when y axis point out magnetic east; x=270 when y axis point out magnetic west
         */
        xCompass = (float) Math.toDegrees(values[0]);

        /** The Pitch
         * y= 0 when the phone is parallel to the floor facing the sky or the floor
         * y=-90 when the phone is perpendicular to the floor, head up;
         * y=90 when the phone is perpendicular to the floor, head down;
         */
        yCompass = (float) Math.toDegrees(values[1]);

        /** The roll
         * z=0 when the phone faces the sky without bending
         * z= -90 when the phone is facing someone,bending left
         * z= 90 when the phone is facing someone,bending right
         * z=180 when the phone faces the floor without bending
         */
        zCompass = (float) Math.toDegrees(values[2]);


    }


    /*********************************************************************/
 /** lightRegister***********************************************/
    /*********************************************************************/

    public void lRegister(String pathFile){


        try {


            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;


            for (int timide=0; timide<cpt-1;timide++)
            {
                val=String.valueOf(lux[timide]);
                output.write(val.getBytes());
                output.write(" ; ".getBytes());

            }

       // toast // enregistrement finalisée



            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    /*********************************************************************/
    /** xRegister***********************************************/
    /*********************************************************************/

    public void xRegister(String pathFile){


        try {


            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;


            for (int timide=0; timide<cpt-1;timide++) {
                valx=String.valueOf(accex[timide]);
                output.write(valx.getBytes());
                output.write(" ; ".getBytes());
            }
            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    /*********************************************************************/
    /** yRegister***********************************************/
    /*********************************************************************/

    public void yRegister(String pathFile){


        try {


            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;


            for (int timide=0; timide<cpt-1;timide++) {
                valy=String.valueOf(accey[timide]);
                output.write(valy.getBytes());
                output.write(" ; ".getBytes());
            }
            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    /*********************************************************************/
    /** zRegister***********************************************/
    /*********************************************************************/

    public void zRegister(String pathFile){


        try {

            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;


            for (int timide=0; timide<cpt-1;timide++) {
                valz=String.valueOf(accez[timide]);
                output.write(valz.getBytes());
                output.write(" ; ".getBytes());
            }
            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    /*********************************************************************/
    /** xcompRegister***********************************************/
    /*********************************************************************/

    public void xcompRegister(String pathFile){


        try {

            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;
            for (int timide=0; timide<cpt-1;timide++) {
                valxC=String.valueOf(xComp[timide]);
                output.write(valxC.getBytes());
                output.write(" ; ".getBytes());
            }

            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    /*********************************************************************/
    /** ycompRegister***********************************************/
    /*********************************************************************/

    public void ycompRegister(String pathFile){


        try {

            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;

            for (int timide=0; timide<cpt-1;timide++) {
                valyC=String.valueOf(yComp[timide]);
                output.write(valyC.getBytes());
                output.write(" ; ".getBytes());
            }
            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    /*********************************************************************/
    /** zcompRegister***********************************************/
    /*********************************************************************/

    public void zcompRegister(String pathFile){


        try {


            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);
            //String liSource=val;

            for (int timide=0; timide<cpt-1;timide++) {
                valzC=String.valueOf(zComp[timide]);
                output.write(valzC.getBytes());
                output.write(" ; ".getBytes());
            }
            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }



    /*********************************************************************/
    /** lat Register***********************************************/
    /*********************************************************************/

    public void latRegister(String pathFile){


        try {

            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);


            for (int timide=0; timide<cpt-1;timide++) {

                val = String.valueOf(latP[timide]);//+String.valueOf(cpt);
                output.write(val.getBytes());
                output.write(" ; ".getBytes());
            }

           // }

            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    /*********************************************************************/
    /** longitude Register***********************************************/
    /*********************************************************************/

    public void lonRegister(String pathFile){


        try {


            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory()+ pathFile);
            FileOutputStream output= new FileOutputStream(linFile);


            for (int timide=0; timide<cpt-1;timide++) {

                val = String.valueOf(longiP[timide]);//+String.valueOf(cpt);
                output.write(val.getBytes());
                output.write(" ; ".getBytes());
            }

            // }

            if(output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    /*********************************************************************/
    /** Values Display***********************************************/
    /*********************************************************************/
    public void lDisplay(String pathFile) {

        try {

            //Déclaration du fichier
            File loutfile = new File(Environment.getExternalStorageDirectory() + pathFile);

            FileInputStream input = new FileInputStream(loutfile);
            BufferedReader linReader = new BufferedReader(new InputStreamReader(input));

            String ligne;

            //On récupère les données ligne par ligne
            while(linReader.ready())
            {
                ligne = linReader.readLine();
                Toast.makeText(getApplicationContext(),""+ligne,Toast.LENGTH_LONG).show();
            }

            linReader.close();
            if(input != null)
                input.close();


        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    /*********************************************************************/
    /** Send Email***********************************************/
    /*********************************************************************/

    protected void sendEmail() {
        // déclaration
        Log.i("Send email", "");
        String[] TO = {""};
        String[] CC = {""};

        // Send intention
        Intent emailIntent = new Intent(Intent.ACTION_SEND);

        text.setText("lux: "+lin.getText().toString()+"\n\t\t xAcc: "+xin.getText().toString()+"\n\t\t yAcc: "+yin.getText().toString()+"\n\t\t zAcc: "+zin.getText().toString()+"\n\t\t xComp: "+xinComp.getText().toString()+"\n\t\t yComp: "+yinComp.getText().toString()+"\n\t\t zComp: "+zinComp.getText().toString());


        // content to send
        emailIntent.setData(Uri.parse("mailto:"));
        emailIntent.setType("text/plain");
        emailIntent.putExtra(Intent.EXTRA_EMAIL, TO);// sender
        emailIntent.putExtra(Intent.EXTRA_CC, CC);
        emailIntent.putExtra(Intent.EXTRA_SUBJECT, "Your subject");// subject
        emailIntent.putExtra(Intent.EXTRA_EMAIL, new String[]{"amoin.massamba@gmail.com"});// receptor
        emailIntent.putExtra(Intent.EXTRA_TEXT,text.getText().toString()); // Message content the measures
        emailIntent.putExtra(android.content.Intent.EXTRA_STREAM, Uri.parse("file://"+getFilesDir()+"/lightdata.txt"));
        // send mail
        startActivity(Intent.createChooser(emailIntent, "Send mail..."));
    }



};
