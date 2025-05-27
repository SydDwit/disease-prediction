import os
import subprocess
import time

def run_evaluations():
    print("=" * 80)
    print("RUNNING COMPLETE MODEL EVALUATION SUITE")
    print("=" * 80)
    
    # Create evaluation directory
    os.makedirs("evaluation_report", exist_ok=True)
    
    # List of scripts to run
    scripts = [
        "generate_confusion_matrix.py",
        "generate_correlation_graphs.py",
        "model_evaluation.py"
    ]
    
    # Run each script
    for script in scripts:
        print("\n" + "=" * 40)
        print(f"RUNNING: {script}")
        print("=" * 40)
        
        try:
            # Run the script using Python
            process = subprocess.run(["python", script], 
                                     capture_output=True, 
                                     text=True, 
                                     check=False)
            
            # Display output
            if process.stdout:
                print("\nOutput:")
                print(process.stdout)
                
            if process.stderr:
                print("\nErrors:")
                print(process.stderr)
                
            # Check if successful
            if process.returncode == 0:
                print(f"\n✅ {script} completed successfully.")
            else:
                print(f"\n❌ {script} failed with return code {process.returncode}.")
                
        except Exception as e:
            print(f"\n❌ Error running {script}: {str(e)}")
        
        # Small delay between scripts
        time.sleep(1)
    
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)
    
    # List generated files
    print("\nGenerated evaluation files:")
    try:
        for file in sorted(os.listdir("evaluation_report")):
            file_path = os.path.join("evaluation_report", file)
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            print(f" - {file} ({file_size:.1f} KB)")
    except Exception as e:
        print(f"Error listing files: {str(e)}")
    
    print("\nTo view the comprehensive HTML report, open:")
    print("evaluation_report/model_evaluation_report.html")

if __name__ == "__main__":
    run_evaluations() 