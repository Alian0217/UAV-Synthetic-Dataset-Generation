import json

report_path = "generated_data/validation_report.json"

with open(report_path, 'r') as f:
    report = json.load(f)

print("=== 详细验证报告 ===")
for check_name, result in report.items():
    print(f"\n{check_name}:")
    print(f"  状态: {'通过' if result['status'] else '失败'}")
    print(f"  总结: {result['summary']}")
    if 'details' in result:
        print("  详细信息:")
        for detail in result['details']:
            print(f"    - {detail}")