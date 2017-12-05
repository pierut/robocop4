until ./cloudbot.sh; do
    echo "Server 'RoboCop' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
