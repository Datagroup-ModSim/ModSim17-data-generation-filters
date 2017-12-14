package org.vadere.simulator.control.org.vadere.simulator.scripts;
import java.io.*;
import java.util.*;
import org.vadere.simulator.entrypoints.ScenarioBuilder;
import org.vadere.simulator.projects.Scenario;
import org.vadere.simulator.projects.ScenarioRun;
import org.vadere.simulator.projects.VadereProject;
import org.vadere.simulator.projects.io.IOVadere;
import java.util.List;


public class VadereAutomaticAllDensity {

    public static int counter = 0;
    public static int maxSpawn = 600;
    public static int totalAmount = 60;
    public static int[][] myArray = new int[31][3];

    public static void main(String[] args) {
        VadereAutomaticAllDensity allDensity = new VadereAutomaticAllDensity();
        allDensity.getDensity("fooK9.csv");

    }

    public void getDensity(String s) {
        //double[][] myArray = new double[231][3];

        int rowC = 0;
        Scanner scanIn = null;
        String fileName = s;
        String Inputline = "";
        try {
            scanIn = new Scanner(new BufferedReader(new FileReader(fileName)));

            while (scanIn.hasNextLine()) {
                Inputline = scanIn.nextLine();
                String[] myArray2 = Inputline.split(",");
                for (int i = 0; i <myArray2.length;i++) {
                    myArray[rowC][i] = Integer.parseInt(myArray2[i]);
                }
                rowC++;
            }
            for (int i = 0; i<myArray.length;i++) {
                int[] temp = myArray[i];
                startCreateOutput(temp);
            }

        }
        catch (Exception e) {
            System.out.print(e);
        }
    }

    public void startCreateOutput(int[] density) throws IOException {

        VadereProject project = IOVadere.readProject("/Users/do/Vadere1/Vadere/dencity");
        Scenario scenario = project.getScenario(0);
        //ScenarioBuilder builder = new ScenarioBuilder(scenario);
        List sourceList = scenario.getTopography().getSources();

        ScenarioBuilder builder2 = new ScenarioBuilder(scenario);

        int h = density[0];
        for (int i=0;i<sourceList.size();i++ ){
                builder2.setSourceField("maxSpawnNumberTotal",i+1,maxSpawn*density[i]/100);

            }

        StringBuilder strBuilder = new StringBuilder();
        for (int i =0; i<density.length;i++){
            strBuilder.append((density[i])+"-");
        }
        String newVerteilung = strBuilder.toString();
        scenario = builder2.build();
        scenario.saveChanges();
        scenario.setName(newVerteilung+"Distribution");
        this.counter = this.counter +1;
        System.out.println(counter);
        new Thread(new ScenarioRun(scenario, s-> increaseCounter())).start();
    }

    public void increaseCounter() {
        if (counter< myArray.length) {

        }
        System.out.println("INCREASE COUNTER: " + counter);
    }
}






