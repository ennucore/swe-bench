#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <case_number>"
  exit 1
fi

case_number=$1

docker rm sweb_container_$case_number


echo "#!/bin/bash" > setup_scr.sh
# Generate the setup script
python3.12 procedure/main.py swe-bench.json $case_number setup >> setup_scr.sh

echo "#!/bin/bash" > eval_scr.sh
# Generate the eval script
python3.12 procedure/main.py swe-bench.json $case_number eval >> eval_scr.sh
python3.12 procedure/main.py swe-bench.json $case_number issue > issue.md

chmod +x setup_scr.sh eval_scr.sh
# Get the repo name
repo_name=$(python3.12 procedure/main.py swe-bench.json $case_number repo)

# Run everything in a single Docker container
docker run -v /Users/ennucore/dev/clippinator:/clippinator -v $(pwd):/mnt --name sweb_container_$case_number -it sweb bash -c "
echo 'setup...'
ls /mnt
cat /mnt/setup_scr.sh

  # Run the setup script
  bash /mnt/setup_scr.sh
  ls /root

  # Run Clippinator
  cd /clippinator && source ~/.bashrc && nvm use 18 && yarn build && ls /root && yarn start simple \"file:/mnt/issue.md\" /${repo_name}

  echo "eval..."

  # Run the eval script
  bash /mnt/eval_scr.sh
" | tee logs/${case_number}.txt

# Clean up temporary files
#rm setup_scr.sh eval_scr.sh

# Remove the Docker container

