# Image Recovery Program
![intro](https://user-images.githubusercontent.com/51738889/138543758-820955ca-10c2-4d58-b016-9c3b9a4c85a8.png)

![image](https://github.com/user-attachments/assets/3a2e695b-13f9-4cc7-84d4-c40d2c3e5a01)

# How to use
1. Download image in question

  `$ python procon32.py download --token=TOKEN`
  
  => What you get
  - problem.ppm

2. Restore an image
  
  `$ python solve.py problem.ppm HEIGHT WIDTH`

  => What you get
  - problem.png
  - fix.png
  - pos.txt
  - rot.txt
  - alt_pos.txt
  - alt_rot.txt
  - size.txt

3. If the image(fix.png) hasn't fully recovered.
  
  ```
  $ cd kaiten
  $ kaiten(debug).exe
  ```

  => The application will launch,and you can manually restore the image.

  => What you get
  - pos.txt (Format: UTF-8 With BOM)
  - rot.txt (Format: UTF-8 With BOM)
  - input.txt ((Format: UTF-8 With BOM)

  <strong>Caution</strong> You need to change the file format to UTF-8.

4. Move the two files(pos.txt, rot.txt) to the parent directory.

5. Solve the puzzle
  
  `$ python ultimate_donyoku.py pos.txt rot.txt`

  => What you get
- solution.txt

6. Verify the image restoration results.
  
  `$ python debuger.py problem.ppm HEIGHT WIDTH`

  => What you get
- debug.png

=> If it(debug.png) has not been restored, change solution.txt manually.

7. Shorten the restore procedure

  `$ python sanitize.py solution.txt`

  => Good results can be obtained.

8. submit file, solution.txt

  `$ python procon32.py submit --token=TOKEN -f solution.txt`
  => What you get
  - Number of incorrect positions.
  - Number of wrong rotations.
