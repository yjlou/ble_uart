=====================
What is the Pipeline?
=====================

This is very similar to the classic Unix pipeline, but it is bi-directional. So it is
more like Python subprocess.Popen.


      +----------+          +----------+          +----------+
      |   NUS    |          |          |          |   ECHO   |
      |          |          |          |          |          |
      |         ---        --------------        ---         |
      |  flow0  out  ===>  in  flow0  out  ===>  in  ==vv    |
      |         ---        -------------         ---         |
      |          |          |          |          |    ||    |
      |         ---        --------------        ---         |
      |  flow1   in  <===  out  flow1  in  <===  out ==<<    |
      |         ---        --------------        ---         |
      |          |          |          |          |          |
      +----------+          +----------+          +----------+
      Process Unit          Process Unit          Process Unit

      <--------------- the pipeline topology ---------------->

Each process unit can consume and emit data. It contains two flows. The first flow (flow0)
is used to consume the data flow from the source (in this case, it is the BLE center).
The second flow (flow1) is used to emit data back to the source.
