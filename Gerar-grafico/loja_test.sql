PGDMP     !    )    
            {         	   loja_test    13.11    13.11     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16985 	   loja_test    DATABASE     i   CREATE DATABASE loja_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Portuguese_Brazil.1252';
    DROP DATABASE loja_test;
                postgres    false            �            1259    16991    vendas    TABLE     �   CREATE TABLE public.vendas (
    nome_vendedor character varying(40) NOT NULL,
    "Desc_venda" text NOT NULL,
    valor money NOT NULL,
    data_venda date NOT NULL
);
    DROP TABLE public.vendas;
       public         heap    postgres    false            �          0    16991    vendas 
   TABLE DATA           P   COPY public.vendas (nome_vendedor, "Desc_venda", valor, data_venda) FROM stdin;
    public          postgres    false    200   S       �   �   x���/>�R!%�X!�41�$����P���(1%5�(QG�s*�,�s�|2+ �b� #=SSN##]C��M,�LTH�WpJ�,*��蔟������WR��V�1	�ts�LP�5����� �s2�     