%===================================================================================================================
%title           : SistSolar.m
%description     : Simulador de N-Cuerpos implementado en el lenguaje Matlab, resuelve por el método de Runge-Kutta.
%author          : Carlos Manuel Rodríguez, Jose Ramón Palacios, Román Perdomo
%usage           : Ejecutar en Matlab o Octave
%notes           : Reportar problemas en "https://github.com/cmrm/fisica-python/issues"
%===================================================================================================================

clear;

%% Posiciones y velocidades iniciales %%
% N debe ser >= 2
N = 9;
r(1,:) = [0 0 0];
r(2,:) = [0.3870 0 0];
r(3,:) = [0.72 0 0];
r(4,:) = [1 0 0];
r(5,:) = [1.52 0 0];
r(6,:) = [5.2 0 0];
r(7,:) = [9.55 0 0];
r(8,:) = [19.22 0 0];
r(9,:) = [30.06 0 0];

v(1,:) = [0 0 0];
v(2,:) = [0 9.9 0];
v(3,:) = [0 7.36 0];
v(4,:) = [0 6.28 0];
v(5,:) = [0 5.08 0];
v(6,:) = [0 2.75 0];
v(7,:) = [0 2.04 0];
v(8,:) = [0 1.44 0];
v(9,:) = [0 1.146 0];

m(1) = 333e3;
m(2) = 0.06;
m(3) = 0.82;
m(4) = 1;
m(5) = 0.11;
m(6) = 318;
m(7) = 95;
m(8) = 14.6;
m(9) = 17.2;

G = 100e-6;
h = 0.00005;
n = 1;
tmin = 0;
tmax = 365;
datos = zeros((tmax-tmin)/h, (N*3));
ePot = zeros((tmax-tmin)/h, 1);
eCin = zeros((tmax-tmin)/h, 1);
tmpVector = tmin : h: tmax-h;
step = 30;      % Datos que se salta a la hora de generar el archivo de salida.

%% Cálculo energía inicial %%
% Energía cinética & potencial
U = 0;
K = 0;
for j = 1:N
    K = K + 0.5*m(j)*(norm(v(j,:))^2);
end

for i = 1:N
    for j = i:N
        if i ~= j
           U = U - G*m(i)*m(j)/norm(r(j,:) - r(i,:));
        end
    end
end

eTotal = U + K;

%% Cálculo de posiciones %% 

for t = tmin : h :(tmax-h)
    % Actualizar posiciones    
    for i = 1:N
        r(i,:) = r(i,:) + v(i,:)*h;
    end

    for i = 1:N
        % Re-calcular velocidades
        for j = 1:N
            if (i ~= j)
                % Runge-Kutta
                k1 = -h*(G*m(j)*(r(i,:)-r(j,:)))/(((r(j,:) - r(i,:))*(r(j,:) - r(i,:))')^(1.5));
                k2 = -h*(G*m(j)*(r(i,:)-r(j,:) + (k1/2)))/(((r(j,:) - r(i,:) + (k1/2))*(r(j,:) - r(i,:) + (k1/2))')^(1.5));
                k3 = -h*(G*m(j)*(r(i,:)-r(j,:) + (k2/2)))/(((r(j,:) - r(i,:) + (k2/2))*(r(j,:) - r(i,:) + (k2/2))')^(1.5));
                k4 = -h*(G*m(j)*(r(i,:)-r(j,:) + k3))/(((r(j,:) - r(i,:) + k3)*(r(j,:) - r(i,:) + k3)')^(1.5));
                v(i,:) = v(i,:) + (k1/6) + (k2/3) + (k3/3) + (k4/6);
            end
        end
    end

    % Energía cinética & potencial
    U = 0;
    K = 0;
    for j = 1:N
        K = K + 0.5*m(j)*(norm(v(j,:))^2);
    end
    
    for i = 1:N
        for j = i:N
            if i ~= j
               U = U - G*m(i)*m(j)/norm(r(j,:) - r(i,:));
            end
        end
    end
    
    ePot(n) = U;
    eCin(n) = K;

    % Almacena posiciones en matriz de datos
    datos(n,:) = [r(1,:) r(2,:) r(3,:) r(4,:) r(5,:) r(6,:) r(7,:) r(8,:) r(9,:)];
    n = n + 1;
end

%% Generar salida de datos para simulación %%

for i = 1:N
    archivo = sprintf('cuerpo_%d.csv', i);
    fdatos = fopen(archivo, 'w+');
    
    counter = 0;
    for j = 1:(n-1)
        if counter > step
            fprintf(fdatos, '%.6f, %.6f, %.6f\n',datos(j,(i*3)-2),datos(j,(i*3)-1),datos(j,(i*3)));
            counter = 0;
        end
        counter = counter + 1;
    end
    fclose(fdatos);
end

fdatos = fopen('potencial.csv', 'w+');
counter = 0;
for i = 1:(n-1)
    if counter > step
        fprintf(fdatos, '%.6f, %.6f\n', tmpVector(i), ePot(i));
        counter = 0;
    end
    counter = counter + 1;
end
fclose(fdatos);

fdatos = fopen('cinetica.csv', 'w+');
counter = 0;
for i = 1:(n-1)
    if counter > step
        fprintf(fdatos, '%.6f, %.6f\n', tmpVector(i), eCin(i));
        counter = 0;
    end
    counter = counter + 1;
end
fclose(fdatos);

fdatos = fopen('error.csv', 'w+');
counter = 0;
for i = 1:(n-1)
    if counter > step
        fprintf(fdatos, '%.6f, %.6f\n', tmpVector(i), abs(eTotal-eCin(i)-ePot(i)));
        counter = 0;
    end
    counter = counter + 1;
end
fclose(fdatos);

%% Gráfica %%

% Posiciones
subplot(1,2,1)
hold on;
plot3(datos(:,1) ,datos(:,2), datos(:,3), 'y');
plot3(datos(:,4), datos(:,5), datos(:,6), 'm');
plot3(datos(:,7), datos(:,8), datos(:,9), 'c');
plot3(datos(:,10), datos(:,11), datos(:,12), 'r');
plot3(datos(:,13), datos(:,14), datos(:,15), 'g');
plot3(datos(:,16), datos(:,17), datos(:,18), 'b');
plot3(datos(:,19), datos(:,20), datos(:,21), 'k');
plot3(datos(:,22), datos(:,23), datos(:,24), 'y');
plot3(datos(:,25), datos(:,26), datos(:,27), 'm');
plot3(0, 0, 0, '*');
title('Posiciones ')
grid on

% Energía
subplot(1,2,2)
hold on;
plot(tmpVector, eCin(:), 'r')
plot(tmpVector, ePot(:), 'g')
plot(tmpVector, ePot(:) + eCin(:), 'b')
title('Energía total del sistema')
legend('Energía cinética','Energía potencial','Energía total')
grid on

