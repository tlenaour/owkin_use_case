json_path = "/tmp/quality_assessment.json"
import matplotlib.pyplot as plt
import json
import click


@click.command()
@click.option('--dataset-quality-assessment-path',
              required=True,
              type=click.Path(exists=True))
@click.option('--output-directory',
              required=True,
              type=click.Path(exists=True))
def main(dataset_quality_assessment_path: str, output_directory: str):
    with open(f"{dataset_quality_assessment_path}") as file:
        data = json.load(file)

    quality_checks = ['is_empty', 'is_format_not_compliant', 'rules']
    total_patients = data["total_patients"]

    for quality_check in quality_checks:
        fig, ax = plt.subplots()
        quality_check_data = data[quality_check]
        total_patient_defected_in_qc = len(quality_check_data["patient_ids_with_defects"])
        defects_by_variables = quality_check_data["defects_by_variables"]
        variables = [key.split("-")[0] for key, value in defects_by_variables.items()]
        counts = list(defects_by_variables.values())
        total_defects = sum(counts)
        ax.bar(variables, counts)
        ax.set_title(f"{quality_check} by variables")
        ax.set_xlabel('Variables')
        ax.set_ylabel('Patients number')
        plt.xticks(rotation=45)
        ax.annotate(f'{total_patient_defected_in_qc} patients with defects over {total_patients} total patients\n{total_defects} defects found',
                    xy=(0.5, 0.5),
                    xycoords='axes fraction',
                    xytext=(0, 0),
                    textcoords='offset points',
                    ha='center', va='center',
                    fontsize=12, color='red')
        plt.tight_layout()
        plt.savefig(f"{output_directory}/{quality_check}.png")
        plt.close()


if __name__ == "__main__":
    main()
