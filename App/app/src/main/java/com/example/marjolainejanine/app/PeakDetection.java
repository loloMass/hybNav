package com.example.marjolainejanine.app;

import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static java.lang.Math.abs;
import static java.lang.Math.sqrt;

/**
 * Created by amassamba on 25/04/2017.
 */

public class PeakDetection  extends AppCompatActivity {
    private TextView nbPics;
    private TextView pics;
    private TextView display;
    private Button read;
    private float l[]={0};

    List<String> tab=new ArrayList<>();    List<Float> lightList=new ArrayList<>();
    List<String> tab1=new ArrayList<>();   List<Float> xList=new ArrayList<>();
    List<String> tab2=new ArrayList<>();   List<Float> yList=new ArrayList<>();
    List<String> tab3=new ArrayList<>();   List<Float> zList=new ArrayList<>();
    List<String> tab4=new ArrayList<>();   List<Float> xCompList=new ArrayList<>();
    List<String> tab5=new ArrayList<>();   List<Float> yCompList=new ArrayList<>();
    List<String> tab6=new ArrayList<>();   List<Float> zCompList=new ArrayList<>();
    List<String> tab7=new ArrayList<>();   List<Float> latList=new ArrayList<>();
    List<String> tab8=new ArrayList<>();   List<Float> longiList=new ArrayList<>();

    List<Float> listAcce=new ArrayList<>();
    List<Integer>multiples28=new ArrayList<>();
    List<List<Float>> acceIntervalles=new ArrayList<>();
    List<Float> acceIntervall=new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_peakdetection);
        nbPics = (TextView) findViewById(R.id.nbPics);
        pics = (TextView) findViewById(R.id.Pics);
        display = (TextView) findViewById(R.id.display);
        read = (Button) findViewById(R.id.read);

        read.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                tab=getListe("/App/lightdata.txt", "light");lightList=string2float(tab);

                tab1=getListe("/App/xdata.txt", "xdata"); xList=string2float(tab1);

                tab2=getListe("/App/ydata.txt", "ydata");yList=string2float(tab2);

                tab3=getListe("/App/zdata.txt", "zdata");zList=string2float(tab3);

                tab4=getListe("/App/xCompdata.txt", "xCompdata");xCompList=string2float(tab4);
                display.setText(xCompList.toString());//Arrays.toString(xCompList)


                tab5=getListe("/App/yCompdata.txt", "yCompdata");yCompList=string2float(tab5);

                tab6=getListe("/App/zCompdata.txt", "zCompdata");zCompList=string2float(tab6);

                tab7=getListe("/App/latdata.txt", "lat"); latList=string2float(tab7);
                display.setText(latList.toString());//Arrays.toString(xCompList)

                tab8=getListe("/App/longidata.txt", "longi"); longiList=string2float(tab8);

                latList=deleteUnusedValues(latList);
                longiList=deleteUnusedValues(longiList);
                lightList=adaptLength(lightList,latList);
                xList=adaptLength(xList,latList);
                yList=adaptLength(yList,latList);
                zList=adaptLength(zList,latList);
                xCompList=adaptLength(xCompList,latList);
                yCompList=adaptLength(yCompList,latList);
                zCompList=adaptLength(zCompList,latList);
                listAcce=tabMoyAcce(xList,yList,zList);

                multiples28=multDiviseur(listAcce,28);
               // acceIntervalles=listIntervalles(listAcce,50,28);
               //acceIntervall =listAcce.subList(28,78);

                for (int i = 0; i < listAcce.size()-1; i++) {
                    //if (i % 28 == 0) {
                            //acceIntervall=listAcce.subList(i, i +50);

                        acceIntervalles.add(listAcce.subList(i, i +50));
                    //}
                }
            }

        });

        //On enlève les valeurs inutiles


    }

private List<String> getListe(String pathFile, String dataName){
    String ligne="";
    List<String> liste=new ArrayList<>();
    //String liste[]=new String[ligne.length()];
    try {

        //Déclaration du fichier
        File loutfile = new File(Environment.getExternalStorageDirectory() + pathFile);

        FileInputStream input = new FileInputStream(loutfile);
        BufferedReader linReader = new BufferedReader(new InputStreamReader(input));


        //On récupère les données ligne par ligne
        while (linReader.ready()) {
            ligne = linReader.readLine();
            String[] items = ligne.split(";");
            liste =  new ArrayList<>(Arrays.asList(items));

            //Toast.makeText(getApplicationContext(), "" + dataName + Arrays.toString(newListe), Toast.LENGTH_LONG).show(); // affichage des valeurs
        }

        linReader.close();
        if (input != null)
            input.close();


    } catch (FileNotFoundException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }
    return liste;
}

private List<Float> string2float(List<String> liste){

    List<Float> newListe=new ArrayList<>();

    //float newListe[] = new float[liste.length]; // Déclaration de la nouvelle liste convertie en float

    for (int i = 0; i < liste.size()-1 ; i++) {
        newListe.add(Float.parseFloat(liste.get(i)));//Float.parseFloat(liste[i]); // conversion des valeurs en float

    }
    return newListe;

}

private List<Float> deleteUnusedValues(List<Float> liste){

    for(int i=0; i<liste.size()-1;i++)
    {
        if (liste.get(i)==0)
        {
            liste.remove(i);
        }
    }

    return liste;

}

private List<Float> adaptLength(List<Float> liste,List<Float> listeGps ){
    int diffTaille=0;
    diffTaille= liste.size()-listeGps.size();
    for (int i=0; i<diffTaille;i++){
        liste.remove(i);
    }

    return liste;
}

private List<Float> tabMoyAcce(List<Float> Xacce,List<Float> Yacce,List<Float> Zacce){
    List<Float> listAcce=new ArrayList<>();
    double j=0;
    for (int i=0; i<Zacce.size();i++){
        j=sqrt(Xacce.get(i)*Xacce.get(i)+Yacce.get(i)*Yacce.get(i)+Zacce.get(i)*Zacce.get(i));
        listAcce.add ((float)j);
    }
    return listAcce;
}



private List<Integer> multDiviseur(List<Float> liste, int diviseur){

    List<Integer>listeMultiples= new ArrayList<>();
    for (int i=0; i<liste.size();i++)
    {
        if( i%diviseur==0 ) {
            listeMultiples.add(i);
        }
    }

    return listeMultiples;
}
private List<List<Float>> listIntervalles(List<Float> liste, int n, int diviseur) {
        List<List<Float>> listeIntervalles = new ArrayList<>();
        List<Float> subb = new ArrayList<>();

        for (int i = 0; i < liste.size()-1; i++) {
            if (i % diviseur == 0) {
                liste.subList(i, i + n);

            }//System.out.println(subb);
        }
        return listeIntervalles;
    }
    /*public float[] retirer(float[] objets) {
        float objet = 0;
        int compt = 0;

        float temp[] = new float[objets.length - 1];

        for (int i = 0; i < objets.length; i++) {
            if (objets[i] == 0) {
                compt = compt + 1;
                temp[i] = objets[i + 1];
                i = i + 1;
            } else {

                temp[i - 1] = objets[i];
            }


        }
        return temp;


    }*/
}