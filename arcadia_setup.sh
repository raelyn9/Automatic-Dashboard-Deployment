# Arcadiua Automation Steps
# Step a) copy table from source to destination
# Step a) invalidate metadata for impala
# Step b) invalidate metadata for arcadia

# init
copy=""
impala=""
arcadia=""
source_db=""
source_tbl=""
dest_db=""
dest_tbl=""
hostname=""

# read configurations
source ./$config.properties

shell_config="-k -i "$hostname
arcadia_shell_cmd=". /opt/cloudera/parcels/ARCADIAENTERPRISE/lib/arcengine/shell/arcadia-shell "$shell_config
impala_shell_cmd="impala-shell "$shell_config
invalidate_cmd="invalidate metadata "$dest_db"."$dest_tbl";"
exit_cmd="exit;"

# create log folder structure if not exists
currentday=$(date +"%Y%m%d")
mkdir -p logs/$currentday

#################################
currenttime=$(date +"%Y%m%d%H%M%S")
logfile_name="logs/"$currentday"/arcadia_setup_"$currenttime".log"
invalidation="logs/"$currentday"/invalidation_"$dest_db"_"$dest_tbl"_"$currenttime".sql"
copy="logs/"$currentday"/copy"$dest_db"_"$dest_tbl"_"$currenttime".sql"

# make a copy the config file in the log folder
copyname=$1"."$currenttime
cp $1 logs/$currentday/$copyname

echo "========= Here is your input ========="
echo "copy table=                  "$copy
echo "invalidation for impala=     "$impala
echo "invalidation for arcadia=    "$arcadia
echo "source database=             "$source_db
echo "source table=                "$source_tbl
echo "destination database=        "$dest_db
echo "destination table=           "$dest_tbl
echo "hostname=                    "$hostname

read -p "The above information is correct? Do you want to go ahead to invalidate metadata accordingly (y/n)?" yn
case $yn in
  [Nn]*) 
         echo "Bye..."
         exit
         ;;
  [Yy]*) 
         echo "Go ahead to invalidate metadata ...."
         ;;
  *) 
         echo "Please answer yes or no."
         exit
         ;;
esac

# Step 0) write invalidate metadata command to file
if test "$impala" = "True" or test "$arcadia" = "True"; then
  echo $invalidate_cmd >> $invalidation

# Step a) copy table from source to destination
if test "$copy" = "True"; then
  echo "###### Copy table from source to destination ###### " >> $logfile_name 
  copy_table="CREATE TABLE "$dest_db"."$dest_tbl" AS SELECT * FROM "$source_db"."$source_tbl";"
  echo $copy_table >> $copy

  copy_table_cmd=$impala_shell_cmd" -f "$copy
  $copy_table_cmd
  echo $copy_table_cmd >> $logfile_name


# Step b) invalidate metadata for impala
if test "$impala" = "True"; then 
  echo "###### Invalidate metadata for Impala ###### " >> $logfile_name 
  impala_invalidation_cmd=$impala_shell_cmd" -f "$invalidation
  echo $impala_invalidation_cmd

  $impala_invalidation_cmd
  echo $impala_invalidation_cmd >> $logfile_name
fi

# Step c) invalidate metadata for arcadia
if test "$arcadia" = "True"; then 
  echo "###### Invalidate metadata for Arcadia ###### " >> $logfile_name 
  arcadia_invalidation_cmd=$arcadia_shell_cmd" -f "$invalidation
  echo $arcadia_invalidation_cmd

  $arcadia_invalidation_cmd
  echo $arcadia_invalidation_cmd >> $logfile_name
fi