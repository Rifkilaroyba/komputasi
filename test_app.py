from app import app

def test_hello_route():
    """
    Fungsi ini menguji endpoint utama ('/') pada aplikasi Flask.
    """
    # Membuat klien tes untuk aplikasi
    client = app.test_client()
    
    # Mengirim permintaan GET ke endpoint '/'
    response = client.get('/')
    
    # Memastikan respons status code adalah 200 (OK)
    assert response.status_code == 200
    
    # Memastikan pesan di dalam respons sesuai dengan yang diharapkan
    assert b"Halo dari Flask + Docker + Jenkins!" in response.data