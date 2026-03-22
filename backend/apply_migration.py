from sqlalchemy import text
from database import engine

def run_migration():
    print("Applying migration_v2.sql...")
    try:
        with open("migration_v2.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()

        # Split by ";" to run one by one (rudimentary split)
        statements = [s.strip() for s in sql_script.split(';') if s.strip()]

        with engine.connect() as connection:
            for stmt in statements:
                try:
                    # Skip empty lines
                    if not stmt:
                        continue
                        
                    connection.execute(text(stmt))
                    connection.commit()
                    print(f"✅ Executed: {stmt.splitlines()[0]}...")
                except Exception as e:
                    # Ignore "already exists" errors safely
                    err_msg = str(e).lower()
                    if "already exists" in err_msg or "duplicate column" in err_msg:
                        print(f"⚠️ Skipped (already exists): {stmt.splitlines()[0]}")
                        continue
                    else:
                        print(f"❌ Failed: {stmt[:50]}... \nError: {e}")
            
            print("🏁 Migration process finished.")

    except Exception as e:
        print(f"❌ specific Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
