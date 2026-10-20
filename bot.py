import os
import random
import subprocess
from datetime import datetime, timedelta

# Configuration
start_date = datetime(2026, 9, 6)
end_date = datetime(2026, 10, 20) # Current date
file_name = "contributions.txt"

# "Less or more" settings: Min and max commits per day
min_commits_per_day = 0
max_commits_per_day = 7 

def make_commit(commit_date):
    # Format date for Git
    date_str = commit_date.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Modify the file to ensure there are unstaged changes
    with open(file_name, 'a') as file:
        file.write(f"Contribution on {date_str}\n")
    
    # Stage the file
    subprocess.run(['git', 'add', file_name], check=True)
    
    # Override environment variables to backdate both Author and Committer timestamps
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    # Execute the commit
    subprocess.run(
        ['git', 'commit', '-m', f"Automated commit for {commit_date.strftime('%Y-%m-%d')}"],
        env=env,
        check=True
    )

def main():
    if not os.path.exists('.git'):
        print("Error: Not a git repository. Run 'git init' first.")
        return

    current_date = start_date
    total_commits = 0
    
    while current_date <= end_date:
        # Determine "less or more" commits for this specific day
        num_commits = random.randint(min_commits_per_day, max_commits_per_day)
        
        for _ in range(num_commits):
            # Spread commits throughout standard working hours
            random_time = current_date + timedelta(
                hours=random.randint(9, 17), 
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            make_commit(random_time)
            total_commits += 1
            
        current_date += timedelta(days=1)
        
    print(f"Successfully generated {total_commits} backdated commits.")
    print("Run 'git remote add origin <your-repo-url>' and 'git push -u origin main' to upload.")

if __name__ == "__main__":
    main()