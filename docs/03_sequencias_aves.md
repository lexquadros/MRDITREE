### **Sequências Comportamentais de Autolimpeza em Falconiformes para Análise Ditree**

O desenvolvimento e a aplicação do **algoritmo MRDITree (Most Reliable Directed Trees)** foram fundamentados em **sequências comportamentais de autolimpeza (self-grooming)**  registradas em **aves da ordem Falconiformes**, complementadas por espécies de Ciconiiformes. Essas sequências são derivadas de um estudo pioneiro descrito na **tese de doutorado de Alexandre Henrique de Quadros (2008)**, intitulada **"Filogenia de falconiformes (aves) baseada em comportamento de autolimpeza"**.
Link da tese de doutorado: https://teses.usp.br/teses/disponiveis/47/47132/tde-06062008-164100/pt-br.html

#### **Origem e Natureza dos Dados**

As sequências comportamentais utilizadas neste trabalho originaram-se de **observações naturalísticas** conduzidas em **treze espécies de aves**, totalizando **3.190 registros de comportamento de autolimpeza**. Essas observações capturaram o **repertório de autolimpeza** em contextos naturais ou semi-naturais, registrando a **ordem e a frequência com que diferentes atos comportamentais ocorrem sequencialmente**. Este tipo de dado é crucial para a análise de **padrões de transição** e **organização interna das sequências**, que são os focos centrais do método Ditree.

#### **Espécies Estudadas**

O estudo original envolveu uma diversidade representativa de **Falconiformes** (gaviões, águias, falcões, caracaras) e **Ciconiiformes** (garças), incluindo:

*   **Família Anatide**: *Aix sponsa* (pato-carolino);
*   **Threskiornithidae**: *Eudocimus ruber* (guará), *Platalea ajaja* (colhereiro);
*   **Família Ardeidae**: *Ardea (=Casmerodius) alba* (Garça-branca-grande);
*   **Família Accipitridae**: *Harpia harpyja* (Harpia), *Buteo albicaudatus* (Gavião-do-rabo-branco), *Buteogallus (=Heterospizias) meridionalis* (gavião-caboclo), *Trigonoceps occipitalis* (Abutre-careca), *Gypohierax angolensis* (Abutre-do-coqueiro);
*   **Família Falconidae**: *Milvago chimachima* (Gavião-pinhé);
*   **Família Cathartidae**: *Coragyps atratus* (Urubu-comum), *Sarcohamphus papa* (urubu-rei) e *Vultur griphus* (condor-andino).

Essa composição inclui espécies de **diferentes regiões geográficas**, abrangendo **tanto as Américas quanto o Velho Mundo**, o que enriquece a base de dados com variações comportamentais potencialmente associadas a diferentes ecologias, filogenias e históricos evolutivos.

#### **Aplicação ao Algoritmo Ditree**

Essas **sequências de autolimpeza**, ricas em transições comportamentais, serviram como **entrada primordial para a análise Ditree**. O algoritmo opera sobre uma **matriz de transição**, calculando **probabilidades condicionais** entre os atos observados. A **primeira ordem de dependência** (Markov de primeira ordem) permite modelar a probabilidade de um ato comportamental ocorrer dado o ato imediatamente anterior. O MRDITree, então, identifica os **caminhos sequenciais mais confiáveis (máximo produto de probabilidades)**, revelando a **estrutura hierárquica e probabilística** subjacente às sequências de grooming.

O uso de dados reais de **comportamento naturalístico**, especialmente de um comportamento tão estereotipado quanto o **autolimpeza**, oferece um **cenário ideal** para aplicar e testar a **eficácia do Ditree**. Ele permite investigar:

*   **Rigidez vs. Flexibilidade Sequencial**: Verificar se certas sequências são altamente estereotipadas ou se permitem variações e decisões contextuais.
*   **Associações Diretas e Substituição Mútua**: Identificar quais atos tendem a ocorrer em sequência e quais podem substituir-se mutuamente em determinados contextos.
*   **Modularidade Comportamental**: Explorar se subsídios da própria sequência comportamental apoiam agrupamentos funcionais ou filogenéticos.
*   **Variação Interspecífica**: Comparar as estruturas de sequência entre as diferentes espécies, buscando padrões evolutivos ou ecológicos.

#### **Relevância e Contribuições**

A utilização das sequências de grooming provenientes da tese de Quadros (2008) confere **robustez empírica** ao algoritmo Ditree desenvolvido. Ao aplicar o MRDITree a esses dados, busca-se não apenas descrever a **organização sequencial do comportamento de autolimpeza** em cada espécie, mas também explorar como essas estruturas podem refletir aspectos da **biologia** e da **história evolutiva** desses táxons. Este tipo de análise **quantitativa e estruturada** do comportamento sequencial contribui para uma **compreensão mais profunda da complexidade e da organização interna dos padrões comportamentais**, complementando abordagens filogenéticas e comparativas.

