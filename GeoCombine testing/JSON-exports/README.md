## Example steps to run Geocombine
1.SSH into the Geoblacklight container 
> docker exec -it geoblacklight_web bash
  
2. Run Interactive Ruby including Geoblacklight module 
> rvm-exec 2.6.6 irb -I . -r geoblacklight
   
3. Open a FGDC xml file in GeoCombine 
> fgdc_metadata =  GeoCombine::Fgdc.new('./geocombine-testing/CAMBRIDGE09_PARCELS.xml')

4. Open an output file to save the results 
> output = File.open( "CAMBRIDGE09_PARCELS.json","w" )

5. Convert FGDC file to GeoBlacklight JSON and save to output file 
> output << fgdc_metadata.to_geoblacklight.to_json

6. Close the output file 
> output.close

7. Exit Interactive Ruby 
> exit

8. Exit Docker shell
> exit
