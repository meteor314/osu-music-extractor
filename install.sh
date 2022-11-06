start_time=$(date +%s)
green_color='\033[0;32m'
red_color='\033[0;31m'
no_color='\033[0m'
home_dir=$(eval echo ~$USER)
osu_path="$home_dir/.local/share/osu"
tmp_path="/tmp/osu-exporter"



# verify if exiftool is installed
if ! command -v exiftool &> /dev/null
then
    echo "exiftool could not be found"
    exit
fi

if [ ! -d "$tmp_path" ]; then
    mkdir "$tmp_path"
    echo -e "${green_color}Created temporary directory${no_color}"
    sleep 2
fi





# welcome message
echo -e "osu! path: $osu_path, ${green_color} start time: $(date)"
echo -e "${no_color}it can take a while to finish, please wait until the script is done"
# go to /home/meteor314/.local/share/osu/ folder and list all files recursively size > 1MB and --mime-type is audio/* and copy them to ~/Music/osu/ folder
if [ ! -d "$osu_path" ]; then
    echo -e "${red_color} folder not found"
    # ask user to input osu! folder path
    read -p "please input osu! folder path: " osu_path
    # verify if user input is valid
    if [ ! -d "$osu_path" ]; then
        echo -e "${red_color}Invalid path"
        exit 1
    fi

fi

#verify if target  folder exist
target_folder="$home_dir/Music/osu"
if [ ! -d "$target_folder" ]; then
    mkdir -p "$target_folder"
    echo -e "${green_color}target folder created : $target_folder"
fi

find $osu_path -type f -size +1M -exec file --mime-type {} \; | grep audio | cut -d: -f1 | xargs -I {} cp {} $tmp_path


# rename all files in target folder with exiftool
while IFS= read -r -d '' file; do 
    #get file name with exiftool
    file_name=$(exiftool -s -s -s -Title "$file")
    #remove only /\:*?"<>| from file name
    file_name=$(echo "$file_name" | sed 's/[\/\\:*?"<>|]//g')
    # move file to target folder with new name
    mv "$file" "$target_folder/$file_name.mp3"
    echo -e "${green_color}file moved: $file_name to $target_folder"
    
done < <(find "$tmp_path" -type f -print0)

echo -e "${green_color}Done..."
sleep 3
echo -e "${no_color} deleting temporary files"
rm -rf "$tmp_path"





echo -e "${green_color}Successfully copied all audio files to $target_folder"
end_time=$(date +%s)
echo -e "${no_color}time elapsed: $((end_time - start_time)) seconds"
