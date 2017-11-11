package org.vadere.simulator.control.org.vadere.simulator.scripts;
import java.util.*;

import org.vadere.simulator.entrypoints.ScenarioBuilder;
import org.vadere.simulator.projects.Scenario;
import org.vadere.simulator.projects.ScenarioRun;
import org.vadere.simulator.projects.VadereProject;
import org.vadere.simulator.projects.io.IOVadere;

import java.nio.file.Paths;
import java.util.List;


public class VadereAutomatic {

    public static void main(String[] args) {
        int amount = 10;
        for (int i =0; i < amount; i++) {
            System.out.println("Start of " + i);
            startAutomatic();
        }
    }

    public static int randomCalc(int min, int max) {
        Random rand = new Random();
        int randomNumber = rand.nextInt(max-min)+min;
        return randomNumber;
    }


    Scenario scene1 = (Scenario) Paths.get("/Users/Do/Documents/Vadere/Vadere/scenarios/OptimalStepM.scenario");


    public static void startAutomatic() {
        try {
            VadereProject project = IOVadere.readProject("/Users/Do/Documents/Vadere/Vadere");
            VadereProject projectJson = IOVadere.readProjectJson("/Users/Do/Documents/Vadere/Vadere");

            Scenario scenario = project.getScenario(0);
           // Scenario JsonScene = projectJson.getScenario(1);

            //ScenarioBuilder builder = new ScenarioBuilder(JsonScene);
            ScenarioBuilder builder2 = new ScenarioBuilder(scenario);

            /*
            JsonScene.getTopography().getSources().get(0).getAttributes().getId();
            builder.setSourceField("id", -1, 2);
            builder.setSourceField("spawnNumber", 2,5);
*/
            int spawnNumber =0;
            for (int i = 0; i <3; i++) {
                spawnNumber += scenario.getTopography().getSources().get(i).getAttributes().getSpawnNumber();
            }

            int spawnNumber1 = randomCalc(0,spawnNumber);
            int spawnNumber2 = randomCalc(0,spawnNumber-spawnNumber1);
            int spawnNumber3 = spawnNumber-(spawnNumber2+spawnNumber1);


            builder2.setSourceField("spawnNumber",1,spawnNumber1);
            builder2.setSourceField("spawnNumber",2,spawnNumber2);
            builder2.setSourceField("spawnNumber",3,spawnNumber3);
            String verteilung = Integer.toString(spawnNumber1)+"-"+Integer.toString(spawnNumber2)+"-"+Integer.toString(spawnNumber3);
            System.out.print(verteilung);

             //JsonScene = builder.build();
             //JsonScene.saveChanges();

            scenario = builder2.build();
            scenario.saveChanges();
            scenario.setName(verteilung+"_Distribution");

            //org.vadere.util.io.IOUtils.writeTextFile("",JsonScene);


            //new Thread(new ScenarioRun(scenario, s -> System.out.print(s + "finished"))).start();
            new Thread(new ScenarioRun(scenario, s -> System.out.print(s + "finished"))).start();

            //Process pr = rt.exec("java -jar /Users/Do/Documents/Vadere/Vadere.jar");
        } catch (Exception e) {
            System.out.println("error" + e.getMessage());
        }
    }
}

