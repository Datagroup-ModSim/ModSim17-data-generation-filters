package org.vadere.simulator.control.org.vadere.simulator.scripts;
import java.util.*;

import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.math3.util.MathArrays;
import org.vadere.simulator.entrypoints.ScenarioBuilder;
import org.vadere.simulator.projects.Scenario;
import org.vadere.simulator.projects.ScenarioRun;
import org.vadere.simulator.projects.VadereProject;
import org.vadere.simulator.projects.io.IOVadere;

import java.nio.file.Paths;
import java.util.List;


public class VadereAutomatic {

    public static int counter = 0;
    public static int maxSpawn = 600;
    public static int totalAmount = 4;
    public static void main(String[] args) {
        VadereAutomatic autom = new VadereAutomatic();
        int amount = 4;
        for (int i =0; i < amount; i++) {
                System.out.println("Start of " + i);
                autom.startAutomaticRand(maxSpawn);

        /*
        Integer[] array = new Integer[]{1,2,3};
        List li = Arrays.asList(array);
        Collections.shuffle(li);
        for (int i = 0; i < li.size();i++) {
            System.out.print(li.get(i));

        }
        */
           // System.out.println("Hier steht der Counter!!!!!!!!!!!!!:"+counter);
        }
        //System.out.println("Hier steht der Counter???:"+counter);
    }

    public static int randomCalc(int min, int max) {
        Random rand = new Random();
        int randomNumber = rand.nextInt(max-min)+min;
        return randomNumber;
    }

    public void startAutomaticRand(int maxSpawnNumber) {
        try {

            VadereProject project = IOVadere.readProject("/Users/do/Vadere1/Vadere");

            Scenario scenario = project.getScenario(3);

            ScenarioBuilder builder2 = new ScenarioBuilder(scenario);


            List sourceList = scenario.getTopography().getSources();

            for (int i=1;i<sourceList.size();i++ ){
                if(i==1) {
                    builder2.setSourceField("maxSpawnNumberTotal",1,maxSpawnNumber);
                }
                builder2.setSourceField("maxSpawnNumberTotal",i+1,0);

            }

            int[] randomArray = new int[sourceList.size()];
            int[] amountPeople = new int[sourceList.size()];
            int people=0;
            int sum = 0;
            int error = 0;
            for (int i = 0; i<randomArray.length;i++) {
                randomArray[i] = randomCalc(0,maxSpawnNumber);
                sum += randomArray[i];
            }

            for (int i = 0; i<randomArray.length;i++) {
                amountPeople[i] = (randomArray[i]*maxSpawnNumber)/sum;
                people += amountPeople[i];
            }
            error = maxSpawnNumber-people;
            int randPos = randomCalc(0,amountPeople.length);
            amountPeople[randPos] += error;


            //int spawnNumber1 = randomCalc(0,maxSpawnNumber);
            //int spawnNumber2 = randomCalc(0,maxSpawnNumber-spawnNumber1);
            //int spawnNumber3 = maxSpawnNumber-(spawnNumber2+spawnNumber1);


            float temp  = (float) maxSpawnNumber;
            /*
            for (int i =1; i< sourceList.size();i++){
                //builder2.setSourceField("id",-1,i);
                builder2.setSourceField("targetIds",i,i);
                builder2.setTargetField("id",-1,i);
            }
            */


            for (int i = 0; i< sourceList.size();i++){
                builder2.setSourceField("maxSpawnNumberTotal",i+1, amountPeople[i]);
            }

            //builder2.setSourceField("maxSpawnNumberTotal",1,spawnNumber1);
            //builder2.setSourceField("maxSpawnNumberTotal",2,spawnNumber2);
            //builder2.setSourceField("maxSpawnNumberTotal",3,spawnNumber3);

            //String verteilung = Float.toString(spawnNumber1/temp)+"-"+Float.toString(spawnNumber2/temp)+"-"+Float.toString(spawnNumber3/temp);


            StringBuilder strBuilder = new StringBuilder();
            for (int i =0; i<amountPeople.length;i++){
                strBuilder.append((amountPeople[i]/temp)+"-");
                //strBuilder.append((amountPeople[i])+"-");
            }
            String newVerteilung = strBuilder.toString();
            scenario = builder2.build();
            scenario.saveChanges();

            //org.vadere.util.io.IOUtils.writeTextFile("",JsonScene);

            scenario.setName(newVerteilung+"Dist");
            //scenario.setName("Distribution");
            //new Thread(new ScenarioRun(scenario, s -> System.out.print(s + "finished"))).start();
            this.counter = this.counter +1;
            System.out.println(counter);

            int testSpawnNumber = 0;
            for (int i = 0; i< sourceList.size();i++) {
                if(scenario.getTopography().getSources().get(i).getAttributes().getId() == i+1) {
                    System.out.println("Die Id müssten passen");
                    testSpawnNumber += scenario.getTopography().getSources().get(i).getAttributes().getMaxSpawnNumberTotal();
                    if (testSpawnNumber == maxSpawnNumber) {
                        System.out.println("Gesamte Anzahl der Menschen passt");
                    }
                }
                /*
                else {
                    System.out.println("ID der Quellen sind falsch vergeben oder die Anzahl der Menschen ist falsch");
                }
                */
            }

           // new Thread(new ScenarioRun(scenario, s-> increaseCounter())).start();
            //Process pr = rt.exec("java -jar /Users/Do/Documents/Vadere/Vadere.jar");
        } catch (Exception e) {
            System.out.println("error" + e.getMessage());
        }
    }

    public void increaseCounter() {
        if (counter< totalAmount) {
            startAutomaticRand(maxSpawn);
        }
        System.out.println("INCREASE COUNTER: " + counter);
    }
}

