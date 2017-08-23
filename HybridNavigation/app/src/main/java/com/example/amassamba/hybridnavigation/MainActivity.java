package com.example.amassamba.hybridnavigation;

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
import android.os.Bundle;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static java.lang.Math.sqrt;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    Button save;

    String val;
    String valz, valxC, valyC, valzC;

    /********************************************************************/
    /** light Sensor attributes***********************************************/
    /*********************************************************************/

    // Light current value
    float l = 0;

    // Sensor manager
    SensorManager sensorManager;

    int cpt = 0; // compteur
    int active = 0;



    /*********************************************************************/
    /** accelerometer Sensor attributes***********************************************/
    /*********************************************************************/

    Sensor accelerometer;
    float  z = 0;

    float accez[] = new float[60000];

    TextView Zacce, steps;
    List<Float> xList = new ArrayList<>();
    List<Float> yList = new ArrayList<>();
    List<Float> zList = new ArrayList<>();
    float indice=0;
    List<Integer> pas = new ArrayList<>();
    List<Float> listAcce = new ArrayList<>();





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // HMI

        //ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);


        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);// SensorManager declaration
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE); //locationManager declaration




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


        /**************************************
         * accelerometer sensor
         * *****************************/

        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER); //accelerometer sensor instantiation

        Zacce = (TextView) findViewById(R.id.Zacce);
        steps = (TextView) findViewById(R.id.steps);
        save=(Button)findViewById(R.id.save);

        /***************************************************************/
        /**Register ************************************/
        /***************************************************************/

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                active = 1;


                zRegister("/App/zdata.txt");

                //Afficher le nombre d'éléments enregistrés à l'appui sur le bouton save
                Toast.makeText(getApplicationContext(), "Enregistrement terminé avec " + String.valueOf(cpt) + " données ", Toast.LENGTH_LONG).show();


            }

        });

    }


    @Override
    protected void onPause() {
        //unregister sensor listener

        sensorManager.unregisterListener((SensorEventListener) this, accelerometer);

        super.onPause();
    }

    @Override
    protected void onResume() {
        // register sensor listener

        sensorManager.registerListener((SensorEventListener) this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
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
         * accelerometer sensor************************
         ********************************/

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {

            z = event.values[2];

            if (active == 0) {
                // enregistrer


                accez[cpt] = z;
                //Conversion and put of x,y,z values on the interface
                cpt = cpt + 1;
                zList.add(z);
                //
                String zValue = String.valueOf(z);
                Zacce.setText(zValue);
                //steps.setText(String.valueOf(pas));
                steps.setText(String.valueOf(zList));
                //indice=moyenne(zList);
               // pas=peakDetection(zList,50,28);
                peakDetection(zList,50,28);

            }

        }

    }


    /*********************************************************************/
    /** zRegister***********************************************/
    /*********************************************************************/

    public void zRegister(String pathFile) {


        try {

            // select the repertory for storage
            File linFile = new File(Environment.getExternalStorageDirectory() + pathFile);
            FileOutputStream output = new FileOutputStream(linFile);
            //String liSource=val;


            for (int t = 0; t < cpt - 1; t++) {
                valz = String.valueOf(accez[t]);
                output.write(valz.getBytes());
                output.write(" ; ".getBytes());
            }
            if (output != null)
                output.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }



    private List<Float> vecteurAcce(List<Float> Xacce, List<Float> Yacce, List<Float> Zacce){
        List<Float> listAcce=new ArrayList<>();
        double j=0;
        for (int i=0; i<Zacce.size();i++){
            j=sqrt(Xacce.get(i)*Xacce.get(i)+Yacce.get(i)*Yacce.get(i)+Zacce.get(i)*Zacce.get(i));
            listAcce.add ((float)j);
        }
        return listAcce;
    }
    private Float moyenne(List<Float> liste){
        int taille =liste.size();
        int somme = 0;

        for(int i = 0; i < taille; i++)
        {
            somme += liste.get(i);
        }
        return (float)somme / taille;

    }


    private List<Integer> maxi(List<Float> liste1){
        List<Integer> indices=new ArrayList<>();

        float acce_zero=moyenne(liste1);
        for (int n=1; n<=11;n++) {
            for (int i=liste1.size()-39;i<liste1.size()-11;i++){
                if (liste1.get(i)> liste1.get(i+n) && liste1.get(i)>liste1.get(i-n) && liste1.get(i)>acce_zero+2.5 ){
                    indices.add(i);
                }
            }
        }
        return indices;
    }
    private List<Integer> peakDetection( List<Float> listeAcce,int intervAnalyse, int diviseur){
        List<List<Float>> listeIntervalles = new ArrayList<>();
        List<List<Integer>> T=new ArrayList<>();
        List<Integer> multiple2diviseur = new ArrayList<>();
        List<Integer> realIndicePics = new ArrayList<>();
        List<Float> picsValues = new ArrayList<>();
        List<Integer>  finalIndicesPics = new ArrayList<>();
        List<Integer> NL=new ArrayList<>();
        for (int i=0; i<listeAcce.size();i++){
            if (i%diviseur==0){
                listeIntervalles.add(listeAcce.subList(i,i+intervAnalyse));
                multiple2diviseur.add(i);
            }
        }
        /*for (int i=0; i<listeIntervalles.size();i++){
              T.add(maxi(listeIntervalles.get(i)));
        }
        for (int i=0; i<T.size();i++){
            for (int j=0; j<T.get(i).size();j++){
                realIndicePics.add(T.get(i).get(j) + multiple2diviseur.get(i));
            }
        }
        for (int k1=0; k1<realIndicePics.size()-1;k1++) {

            picsValues.add(listeAcce.get(realIndicePics.get(k1)));

            if ((realIndicePics.get(k1 + 1) - realIndicePics.get(k1) > 5) && (listeAcce.get(realIndicePics.get(k1)) >listeAcce.get(realIndicePics.get(k1)))){
                finalIndicesPics.add(realIndicePics.get(k1));
                }
            else if ((realIndicePics.get(k1 + 1) - realIndicePics.get(k1) > 5) && (listeAcce.get(realIndicePics.get(k1)) <listeAcce.get(realIndicePics.get(k1)))){
                finalIndicesPics.add(realIndicePics.get(k1+1));
            }
            else if ((realIndicePics.get(k1 + 1) - realIndicePics.get(k1) < 5 )&& (listeAcce.get(realIndicePics.get(k1)) <listeAcce.get(realIndicePics.get(k1)))){
                finalIndicesPics.add(realIndicePics.get(k1));
            }

        }
        for (int j=0; j<finalIndicesPics.size()-1;j++){
            if( (!(finalIndicesPics.get(j)).equals(finalIndicesPics.get(j+1))) && (finalIndicesPics.get(j+1) - finalIndicesPics.get(j) > 15)){
                NL.add(finalIndicesPics.get(j));
            }
        }
*/

        return NL;
    }


};
