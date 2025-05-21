rm -rf /opt/ANDRAX/homepwn
rm -rf /opt/ANDRAX/HomePWN

cd ./utils && unzip swig.zip && cd swig
echo ${PWD##*/}
if [ ${PWD##*/} == "swig" ] 
then
    find . -exec touch {} \;
    make clean
    ./configure --without-tcl

    if [ $? -eq 0 ]
    then
      # Result is OK! Just continue...
      echo "Configure swig... PASS!"
    else
      # houston we have a problem
      exit 1
    fi

    make

    if [ $? -eq 0 ]
    then
      # Result is OK! Just continue...
      echo "Make swig... PASS!"
    else
      # houston we have a problem
      exit 1
    fi

    make install

    if [ $? -eq 0 ]
    then
      # Result is OK! Just continue...
      echo "Make install swig... PASS!"
    else
      # houston we have a problem
      exit 1
    fi

    cd ..
    rm -r swig*
    cd ..
fi

rm -rf Papers

python3 -m venv /opt/ANDRAX/homepwn

source /opt/ANDRAX/homepwn/bin/activate

/opt/ANDRAX/homepwn/bin/bin/pip3 install setuptools==41.6.0
/opt/ANDRAX/homepwn/bin/bin/pip3 install -r modules/_requirements.txt

if [ $? -eq 0 ]
then
  # Result is OK! Just continue...
  echo "Install module requirements... PASS!"
else
  # houston we have a problem
  exit 1
fi

cp -Rf $(pwd) /opt/ANDRAX/homepwn/package

if [ $? -eq 0 ]
then
  # Result is OK! Just continue...
  echo "Copy PACKAGE... PASS!"
else
  # houston we have a problem
  exit 1
fi

cp -Rf andraxbin/* /opt/ANDRAX/bin
