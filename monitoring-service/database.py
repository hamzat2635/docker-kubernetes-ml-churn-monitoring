import os
import psycopg


# These values are replaced by environment variables in Kubernetes
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "churndb")
DB_USER = os.getenv("DB_USER", "clouduser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "cloudpass")


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5
    )


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            prediction VARCHAR(20),
            churn_probability FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tenure INTEGER,
            internet_service VARCHAR(50),
            contract VARCHAR(50),
            monthly_charges FLOAT,
            total_charges FLOAT,
            tech_support VARCHAR(50),
            online_security VARCHAR(50),
            paperless_billing VARCHAR(10),
            payment_method VARCHAR(100)
        )
        """
    )

    connection.commit()
    cursor.close()
    connection.close()


def save_prediction(customer, prediction, churn_probability):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            prediction,
            churn_probability,
            tenure,
            internet_service,
            contract,
            monthly_charges,
            total_charges,
            tech_support,
            online_security,
            paperless_billing,
            payment_method
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """,
        (
            prediction,
            churn_probability,
            customer.tenure,
            customer.InternetService,
            customer.Contract,
            customer.MonthlyCharges,
            customer.TotalCharges,
            customer.TechSupport,
            customer.OnlineSecurity,
            customer.PaperlessBilling,
            customer.PaymentMethod
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_predictions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            prediction,
            churn_probability,
            created_at,
            tenure,
            internet_service,
            contract,
            monthly_charges,
            total_charges,
            tech_support,
            online_security,
            paperless_billing,
            payment_method
        FROM predictions
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    predictions = []

    for row in rows:
        predictions.append(
            {
                "id": row[0],
                "prediction": row[1],
                "churn_probability": row[2],
                "created_at": row[3],
                "tenure": row[4],
                "InternetService": row[5],
                "Contract": row[6],
                "MonthlyCharges": row[7],
                "TotalCharges": row[8],
                "TechSupport": row[9],
                "OnlineSecurity": row[10],
                "PaperlessBilling": row[11],
                "PaymentMethod": row[12]
            }
        )

    return predictions
