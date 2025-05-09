# grex-T3
Related code to GReX-T3

To use this ````cand_plotter_restart.service``` and allow the Python script to restart the ```cand_plotter.service```, you have to update the sudoers file by
1. Open the sudoers file by visudo
```
sudo visudo
```
2. Add the following line to the bottom of the file
```
user ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart cand_plotter.service
```
3. Check the path by ```which systemctl``` if you use a different path for systemctl 
