#!/usr/bin/bash

user=$(awk -F':' '{ print $1}' users)


for i in $user
do


  a=$(($a+1))
  h=$(cat users | awk -F':' '{ print $3}' users | head -n $a | tail -n 1)
  g=$(cat users | awk -F':' '{ print $5}' users | head -n $a | tail -n 1)
  p=$(cat users | awk -F':' '{ print $4}' users | head -n $a | tail -n 1)


      for gr in $g
       do
             if  grep -q $gr /etc/group
              then
                echo " Groups already exist !!! "
             else
              groupadd "$gr"
              echo "Groups added Successfully ......"
             fi
      done;

echo "-----------------------------------------------"


  if  grep -q $i /etc/passwd
   then
    echo " Users already exist !!! "

  else
    useradd "$i" -d "$h" -g "$g"
  fi

      if grep -q $i /etc/passwd
        then
                echo " Password not changing becasuse users allready exist !!!"
        else

                echo "$p" | passwd --stdin "$i"
                echo "--------------------------------------------------"
                echo "Name: $i"
                echo "Home: $h"
                echo "Password: $p"
                echo "Group: $g"
                echo "--------------------------------------------------"
                echo "Users created succussfully !!!  BY Nicat Mansimov"
      fi
done
