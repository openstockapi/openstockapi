import openstockapi as osapi

def main():
    # Khoi tao session voi API key Pro mau
    osapi.init(api_key="pro_sample_key")

    print("=========================================================")
    print("      OpenStockAPI - Demo Vietnam Derivatives Data       ")
    print("=========================================================")

    # 1. Hop dong tuong lai VN30F1M
    print("\n[1] Get Future Profile (VN30F1M):")
    try:
        future_prof = osapi.derivative_profile("VN30F1M")
        for k, v in future_prof.items():
            print(f"  - {k:<22}: {v}")
    except Exception as e:
        print(f"  [Error] {e}")

    # 2. Chung quyen CHPG2401
    print("\n[2] Get Warrant Profile (CHPG2401):")
    try:
        warrant_prof = osapi.derivative_profile("CHPG2401")
        for k, v in warrant_prof.items():
            print(f"  - {k:<22}: {v}")
    except Exception as e:
        print(f"  [Error] {e}")

if __name__ == "__main__":
    main()
